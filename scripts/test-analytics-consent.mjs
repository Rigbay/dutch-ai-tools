import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import ts from 'typescript';

const source = fs.readFileSync(new URL('../src/lib/analyticsConsent.ts', import.meta.url), 'utf8');
const policy = fs.readFileSync(new URL('../src/lib/analyticsPolicy.ts', import.meta.url), 'utf8');
assert.match(policy, /ready: false/);
assert.match(policy, /consentVersion: 1/);
assert.match(policy, /analyticsPolicy\.consentVersion > 1/);
const KEY = 'dat_analytics_consent';
const TTL = 180 * 86400000;
const NOW = 1788780000000;
const consent = (choice = 'granted', version = 2, expiresAt = NOW + TTL) => JSON.stringify({version, choice, savedAt: expiresAt - TTL, expiresAt});

class Node {
  hidden = false; dataset = {}; textContent = ''; listeners = {}; removed = false;
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  dispatch(type, extra = {}) { for (const fn of this.listeners[type] || []) fn({target: this, ...extra}); }
  focus() { this.focused = true; }
  remove() { this.removed = true; }
}
class Anchor extends Node { closest() { return this; } }

function setup({ready = true, version = 2, stored, localReadFails = false, localWriteFails = false, sessionFails = false, cookieFails = false, qa = '', host = 'example.test'} = {}) {
  const store = new Map(stored === undefined ? [] : [[KEY, stored]]);
  const session = new Map(); const scripts = []; const timers = new Map();
  const elements = Object.fromEntries(['status','heading','accept','reject','close','open','panel'].map(name => [name,new Node()]));
  const selectors = {'[data-consent-status]':'status','#consent-heading':'heading','[data-consent-accept]':'accept','[data-consent-reject]':'reject','[data-consent-close]':'close'};
  elements.panel.querySelector = s => elements[selectors[s]];
  const document = new Node();
  document.querySelector = () => elements.panel;
  document.querySelectorAll = () => [elements.open];
  document.createElement = () => new Node();
  document.head = {appendChild: script => scripts.push(script)};
  document.referrer = 'https://referrer.test/page?private=value';
  const cookies = new Map([['_ga','old'],['_ga_P1DQLR76C6','old'],['unrelated','keep']]);
  Object.defineProperty(document,'cookie',{get(){if(cookieFails) throw Error('blocked');return [...cookies].map(([k,v])=>`${k}=${v}`).join('; ');},set(value){if(cookieFails) throw Error('blocked'); cookies.delete(value.split('=')[0]);}});
  const window = new Node();
  const location = {hostname:host,pathname:'/article/',origin:`https://${host}`,href:`https://${host}/article/?secret=private`,search:qa,reloads:0,reload(){this.reloads++;}};
  let time = NOW;
  class Clock extends Date { static now(){return time;} }
  const context = {window,document,location,URL,URLSearchParams,Element:Node,HTMLAnchorElement:Anchor,Date:Clock,
    localStorage:{getItem(key){if(localReadFails) throw Error('blocked');return store.get(key)??null;},setItem(key,value){if(localWriteFails) throw Error('blocked');store.set(key,value);},removeItem(key){if(localWriteFails) throw Error('blocked');store.delete(key);}},
    sessionStorage:{getItem(key){if(sessionFails) throw Error('blocked');return session.get(key)??null;},setItem(key,value){if(sessionFails) throw Error('blocked');session.set(key,value);},removeItem(key){if(sessionFails) throw Error('blocked');session.delete(key);}},
    setTimeout(fn){const id=timers.size+1;timers.set(id,fn);return id;},clearTimeout(id){timers.delete(id);},
  };
  const injected = source.replace(/^import[^\n]+\n/,`const analyticsPolicy = ${JSON.stringify({ready,consentVersion:version})}; const analyticsReady = analyticsPolicy.ready && analyticsPolicy.consentVersion > 1;\n`).replace('export function initializeAnalyticsConsent','function initializeAnalyticsConsent');
  const compiled = ts.transpileModule(injected,{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.None}}).outputText.replace(/export \{\};?\s*$/,'');
  vm.runInNewContext(compiled+'\ninitializeAnalyticsConsent();',context);
  return {elements,store,scripts,cookies,window,document,location,timers,setTime(value){time=value;},blockStorage(){localWriteFails=true;sessionFails=true;},click(name){elements[name].dispatch('click');},affiliate(){const a=new Anchor();a.dataset={affiliateMerchant:'make',affiliateSite:'dutch-ai-tools'};a.href='https://www.make.com/en/register?pc=hermesai';document.dispatch('click',{target:a});return a;}};
}

let cases=0;
function test(name,fn){fn();cases++;console.log(`PASS ${name}`);}
test('suspension ignores even a valid grant and saves no choice',()=>{const x=setup({ready:false,stored:consent()});x.click('accept');x.affiliate();assert.equal(x.scripts.length,0);assert.equal(x.elements.panel.hidden,true);assert.equal(x.store.get(KEY),consent());assert.equal(x.cookies.has('_ga'),false);assert.equal(x.cookies.get('unrelated'),'keep');});
test('version 1 cannot activate even if readiness is switched',()=>assert.equal(setup({ready:true,version:1,stored:consent('granted',1)}).scripts.length,0));
test('first visit has no tag or pre-consent event queue',()=>{const x=setup();x.affiliate();assert.equal(x.scripts.length,0);assert.equal(x.window.dataLayer.length,0);assert.equal(x.elements.panel.hidden,false);});
test('reject persists without loading a tag',()=>{const x=setup();x.click('reject');assert.equal(JSON.parse(x.store.get(KEY)).choice,'denied');assert.equal(x.scripts.length,0);assert.equal(x.elements.panel.hidden,true);});
test('accept loads once with ads denied and no query in page/referrer',()=>{const x=setup();x.click('accept');x.click('accept');assert.equal(x.scripts.length,1);const calls=x.window.dataLayer.map(v=>Array.from(v));assert.equal(calls[0][2].analytics_storage,'granted');assert.equal(calls[0][2].ad_storage,'denied');assert.equal(calls[2][2].page_location,'https://example.test/article/');assert.equal(calls[2][2].page_referrer,'https://referrer.test/page');});
test('partner event only follows consent; navigation URL is unchanged',()=>{const x=setup();x.click('accept');const a=x.affiliate();const call=Array.from(x.window.dataLayer.at(-1));assert.equal(call[1],'affiliate_outbound_click');assert.equal(call[2].link_url,'https://www.make.com/en/register');assert.equal(a.href,'https://www.make.com/en/register?pc=hermesai');});
test('withdraw disables synchronously, clears cookies and reloads without denied ping',()=>{const x=setup();x.click('accept');x.cookies.set('_ga','new');x.click('open');assert.equal(x.elements.heading.focused,true);x.click('reject');x.affiliate();assert.equal(x.window['ga-disable-G-P1DQLR76C6'],true);assert.equal(x.window.dataLayer.length,0);assert.equal(x.scripts[0].removed,true);assert.equal(x.location.reloads,1);assert.equal(x.cookies.has('_ga'),false);assert.equal(JSON.parse(x.store.get(KEY)).choice,'denied');});
test('return with refusal does not show a banner or load GA',()=>{const x=setup({stored:consent('denied')});assert.equal(x.scripts.length,0);assert.equal(x.elements.panel.hidden,true);});
test('old-version, malformed, future and expired grants are invalid',()=>{for(const stored of [consent('granted',1),'broken',consent('granted',2,NOW-1),consent('granted',2,NOW+TTL+1000)])assert.equal(setup({stored}).scripts.length,0);});
test('read/storage-write failures fail closed',()=>{for(const opts of [{localReadFails:true},{localWriteFails:true},{stored:consent(),localWriteFails:true}]){const x=setup(opts);x.click('accept');assert.equal(x.scripts.length,0);assert.match(x.elements.status.textContent,/niet opslaan/);}});
test('session storage and cookie failures do not crash or load GA',()=>{assert.equal(setup({sessionFails:true,stored:consent()}).scripts.length,0);const x=setup({cookieFails:true});x.click('reject');assert.equal(x.scripts.length,0);});
test('QA and localhost exclusions override consent',()=>{for(const opts of [{qa:'?orbit_qa=1'},{host:'localhost'},{host:'127.0.0.1'}]){const x=setup({...opts,stored:consent()});assert.equal(x.scripts.length,0);}});
test('cross-tab withdrawal stops an active page',()=>{const x=setup({stored:consent()});x.store.set(KEY,consent('denied'));x.window.dispatch('storage',{key:KEY});assert.equal(x.location.reloads,1);assert.equal(x.window['ga-disable-G-P1DQLR76C6'],true);});
test('failed withdrawal persistence cannot reload a stale grant',()=>{const x=setup({stored:consent()});x.blockStorage();x.click('reject');assert.equal(x.location.reloads,0);assert.equal(x.window['ga-disable-G-P1DQLR76C6'],true);assert.equal(x.window.dataLayer.length,0);assert.equal(x.scripts[0].removed,true);});
test('losing storage during use disables without reloading into an old grant',()=>{const x=setup({stored:consent()});x.blockStorage();x.affiliate();assert.equal(x.location.reloads,0);assert.equal(x.window['ga-disable-G-P1DQLR76C6'],true);assert.equal(x.window.dataLayer.length,0);});
test('expiry and restored-page consent are rechecked',()=>{const x=setup({stored:consent()});x.setTime(NOW+TTL+1);x.window.dispatch('pageshow',{persisted:true});assert.equal(x.location.reloads,1);assert.equal(x.window['ga-disable-G-P1DQLR76C6'],true);});
test('closing never implies consent; settings reopen and focus returns',()=>{const x=setup();x.click('close');assert.equal(x.store.has(KEY),false);x.click('open');x.click('close');assert.equal(x.elements.open.focused,true);assert.equal(x.scripts.length,0);});
console.log(`${cases} consent behavior cases passed. No network requests were made by these isolated tests.`);
