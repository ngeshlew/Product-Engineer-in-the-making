# Protection

Advisory protection markers help preserve critical code. Use comment markers around regions:

- PROTECTED: `!cp` ... `END-P`
- GUARDED: `!cg` ... `END-G`
- INFO: `!ci` ... `END-I`
- DEBUG: `!cd` ... `END-D`
- TEST: `!ct` ... `END-T`
- CRITICAL: `!cc` ... `END-C`

Example (JS):
```js
// !cp PROTECTED - DO NOT MODIFY
function critical() {}
// !cp END-P
```

See: `.cursor/rules/code-protection.mdc` and `docs/ripersigma/ProtectionCommands.md`