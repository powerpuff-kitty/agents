## OpenCode host guidance

- Use the project instructions and relevant skills actually available in this
  OpenCode session. Do not assume a particular integration, skill catalog, or model.
- Native skills are SKILL.md resources discovered by OpenCode. The profile
  renderer does not install them or alter skill permissions; inspect the actual
  available inventory and load only the relevant procedure.
- Native browser access depends on the host and can be denied. Use existing local
  browser tests, screenshots, or accessibility tooling when available and authorized;
  otherwise preserve unverified visual/interaction checks. Do not override global
  permissions merely to finish a review.
- Profile instructions do not enforce a read-only sandbox. Respect configured
  permissions and current task authorization. Selecting a profile does not itself
  authorize publication, deployment, tracker changes, or other external actions.
- A denied compound shell command does not establish that its executables are
  unavailable. Use the supported working-directory field and separate already
  permitted checks when appropriate; keep denied operations denied. Interpret
  tool completion together with result errors and process exits: a completed
  wrapper can still contain a failed or unexecuted check.
