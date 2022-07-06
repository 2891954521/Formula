package com.machine.learning

import java.io.*
import java.net.HttpURLConnection
import java.net.URL

object WebUtil {

    fun inputStream2string(inputStream: InputStream): String {
        return try {
            val outStream = ByteArrayOutputStream()
            val buffer = ByteArray(1024)
            var len: Int
            while(inputStream.read(buffer).also { len = it } != -1) outStream.write(buffer, 0, len)
            outStream.toString()
        } catch(e: IOException) {
            ""
        } finally {
            inputStream.close()
        }
    }

    @Throws(IOException::class)
    fun doGet(url: String?, cookie: String?, vararg params: String?): String {
        val connection = get(url, cookie, *params)
        return if(connection.responseCode == HttpURLConnection.HTTP_OK) {
            inputStream2string(connection.inputStream)
        } else ""
    }

    @Throws(IOException::class)
    operator fun get(url: String?, cookie: String?, vararg params: String?): HttpURLConnection {
        val connection = URL(url).openConnection() as HttpURLConnection
        connection.instanceFollowRedirects = false
        connection.requestMethod = "GET"
        if(cookie != null) connection.setRequestProperty("Cookie", cookie)
        if(params.isNotEmpty()) {
            var i = 0
            while(i < params.size) {
                connection.setRequestProperty(params[i], params[i + 1])
                i += 2
            }
        }
        connection.connect()
        return connection
    }

    @Throws(IOException::class)
    fun doPost(url: String?, cookie: String?, data: String, vararg params: String?): String {
        val connection = post(url, cookie, data, *params)
        return if(connection.responseCode == HttpURLConnection.HTTP_OK) {
            inputStream2string(connection.inputStream)
        } else ""
    }

    @Throws(IOException::class)
    fun post(url: String?, cookie: String?, data: String, vararg params: String?): HttpURLConnection {
        val connection: HttpURLConnection = URL(url).openConnection() as HttpURLConnection
        connection.doOutput = true
        connection.instanceFollowRedirects = false
        connection.requestMethod = "POST"
        if(cookie != null) connection.setRequestProperty("Cookie", cookie)
        if(params.isNotEmpty()) {
            var i = 0
            while(i < params.size) {
                connection.setRequestProperty(params[i], params[i + 1])
                i += 2
            }
        }
        connection.outputStream.write(data.toByteArray())
        connection.connect()
        return connection
    }

    fun uploadFile(uploadUrl: String?, file: File): String {

        val end = "\r\n"
        val twoHyphens = "--"
        val boundary = "---------------------------823928434"
        try {
            val len = file.length().toInt()
            val bytes = ByteArray(len)
            val reader = FileInputStream(file)
            reader.read(bytes, 0 ,len)
            reader.close()

            val url = URL(uploadUrl)
            val connection = url.openConnection() as HttpURLConnection
            connection.doInput = true
            connection.doOutput = true
            connection.useCaches = false
            connection.requestMethod = "POST"
            connection.setRequestProperty("Connection", "Keep-Alive")
            connection.setRequestProperty("Charset", "UTF-8")
            connection.setRequestProperty("Content-Type", "multipart/form-data;boundary=$boundary")
            val dos = DataOutputStream(connection.outputStream)
            dos.writeBytes(twoHyphens + boundary + end)
            dos.writeBytes("Content-Disposition: form-data; name=\"image\"; filename=\"image.jpg\"$end")
            dos.writeBytes(end)
            dos.write(bytes)
            dos.writeBytes(end)
            dos.writeBytes(twoHyphens + boundary + twoHyphens + end)
            dos.flush()

            return if(connection.responseCode == HttpURLConnection.HTTP_OK){ inputStream2string(connection.inputStream) }else{ "" }

        } catch(e: Exception) {
            e.printStackTrace()
        }
        return ""
    }
}