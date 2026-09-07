// Containment release: do not activate until the controller, processing facts,
// notice and consent handling have been verified and independently reviewed.
// Activation MUST change consentVersion; an earlier preference cannot activate GA.
export const analyticsPolicy = {
  ready: false,
  consentVersion: 1,
} as const;
// Version 1 belongs only to the suspended release. Enabling requires a new version.
export const analyticsReady = analyticsPolicy.ready && analyticsPolicy.consentVersion > 1;
