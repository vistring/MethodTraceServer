package com.xiaojinzi.tallyserver.util

import okio.ByteString.Companion.toByteString
import java.security.MessageDigest


fun String.md5(): String {
    // 对 String 做 md5 编码
    val md = MessageDigest.getInstance("MD5")
    val digest = md.digest(this.toByteArray())
    return digest.toByteString().hex()
}