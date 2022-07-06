package com.machine.learning

import android.Manifest
import android.app.ProgressDialog
import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.MediaStore
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.content.FileProvider
import androidx.core.view.WindowCompat
import com.google.android.material.snackbar.Snackbar
import com.machine.learning.databinding.ActivityMainBinding
import com.yalantis.ucrop.UCrop
import com.yalantis.ucrop.UCropActivity
import org.json.JSONObject
import java.io.File
import kotlin.concurrent.thread


class MainActivity : AppCompatActivity() {

    // 如果勾选了不再询问
    private val NOT_NOTICE: Int = 1
    // 拍照
    private val TAKE_PHOTO: Int = 233

    private val CROP_PHOTO: Int = 234

    private val REQUEST_PERMISSION: Int = 666


    private lateinit var photoUri: Uri

    private lateinit var cropUri: Uri

    private lateinit var photoFile: File

    private lateinit var cropFile: File

    private lateinit var address: String

    private lateinit var sp: SharedPreferences

    private lateinit var binding: ActivityMainBinding

    private lateinit var dialog: ProgressDialog

    override fun onCreate(savedInstanceState: Bundle?) {
        WindowCompat.setDecorFitsSystemWindows(window, false)
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        setSupportActionBar(binding.toolbar)

        sp = getSharedPreferences("data", Context.MODE_PRIVATE)

        address = sp.getString("serverIP", "") ?: ""

        photoFile  = File(externalCacheDir, "pic.jpg")
        cropFile  = File(externalCacheDir, "crop.jpg")

        binding.inputServerIp.editText?.setText(address)

        binding.buttonShoot.setOnClickListener {
            if(binding.inputServerIp.editText?.editableText.toString().also { address = it }.isEmpty()){
                binding.inputServerIp.error = "请输入服务API地址"
            }else{
                binding.inputServerIp.error = null
                takePicture()
            }
        }

        dialog = ProgressDialog(this)
        dialog.setMessage("正在上传文件")
        dialog.setCancelable(true)
    }

    private fun takePicture() {

        if(ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CAMERA), REQUEST_PERMISSION)
            return
        }

        val intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)

        if(Build.VERSION.SDK_INT > 24) {
            intent.flags = Intent.FLAG_GRANT_WRITE_URI_PERMISSION
            photoUri = FileProvider.getUriForFile(this, packageName, photoFile)
        } else {
            // 从文件中创建uri
            photoUri = Uri.fromFile(photoFile)
        }

        cropUri = Uri.fromFile(cropFile)


        intent.putExtra(MediaStore.EXTRA_OUTPUT, photoUri)
        startActivityForResult(intent, TAKE_PHOTO)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if(requestCode == NOT_NOTICE) {
            // 由于不知道是否选择了允许所以需要再次判断
            if(ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CAMERA), REQUEST_PERMISSION)
            }
            return
        }

        if(resultCode != RESULT_OK) {
            return
        }else if(resultCode == UCrop.RESULT_ERROR) {
            if(data == null) return
            Snackbar.make(
                binding.buttonShoot,
                UCrop.getError(data).toString(),
                Snackbar.LENGTH_SHORT
            ).show()
            return
        }

        if(requestCode == TAKE_PHOTO) {
            val options = UCrop.Options()
            options.setToolbarTitle("裁剪图片")
            options.setCompressionQuality(75)
            //隐藏下边控制栏
            options.setHideBottomControls(true)
            //设置是否显示裁剪网格
            options.setShowCropGrid(true)
            //设置是否显示裁剪边框(true为方形边框)
            options.setShowCropFrame(true)
            options.setFreeStyleCropEnabled(true)
            UCrop.of(photoUri, cropUri).withOptions(options).start(this);
            return
        }else if(requestCode == UCrop.REQUEST_CROP) {
            if(data == null) return
            cropUri = UCrop.getOutput(data) as Uri
        }

        if(!address.startsWith("http://")){
                address = "http://$address";
        }

        sp.edit().putString("serverIP", address).apply()

        dialog.show()

        thread {
            try {
                val json = JSONObject(WebUtil.uploadFile(address, cropFile))
                runOnUiThread {
                    if(json.get("code") == 200) {
                        if(json.has("formula") && json.has("result")){
                            binding.inputFormula.editText?.setText(json.getString("formula"))
                            binding.inputResult.editText?.setText(json.getString("result"))
                        }
                    }
                    dialog.dismiss()
                    Snackbar.make(
                        binding.buttonShoot,
                        json.getString("msg"),
                        Snackbar.LENGTH_SHORT
                    ).show()
                    // Toast.makeText(this, json.getString("msg"), Toast.LENGTH_SHORT).show()
                }
            }catch(e: Exception){
                runOnUiThread {
                    Toast.makeText(this, "error:" + e.message, Toast.LENGTH_SHORT).show()
                }
            }
        }

    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        // Inflate the menu; this adds items to the action bar if it is present.
        menuInflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        return when(item.itemId) {
            R.id.action_settings -> true
            else -> super.onOptionsItemSelected(item)
        }
    }
}