#!/usr/bin/env node
/**
 * 標準入力の文字列を AES-256-GCM で暗号化して base64 を出力する。
 * 使い方: echo '...' | node encrypt-blob.js <password>
 * 形式は encrypt-answers.js と同じ（salt16 + iv12 + tag16 + 暗号文）。
 */
'use strict';
const crypto = require('crypto');
const password = process.argv[2];
if (!password) { console.error('usage: node encrypt-blob.js <password>'); process.exit(1); }
let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', d => input += d);
process.stdin.on('end', () => {
  const salt = crypto.randomBytes(16);
  const key = crypto.pbkdf2Sync(password, salt, 100000, 32, 'sha256');
  const iv = crypto.randomBytes(12);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const enc = Buffer.concat([cipher.update(input, 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();
  process.stdout.write(Buffer.concat([salt, iv, tag, enc]).toString('base64'));
});
