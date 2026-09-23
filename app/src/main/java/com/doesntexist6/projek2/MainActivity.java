package com.doesntexist6.projek2;

import android.os.Bundle;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private EditText inputTelepon;
    private RadioGroup grupPilihan;
    private android.widget.Button tombolTampil;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        inputTelepon = findViewById(R.id.etNomorTelepon);
        grupPilihan = findViewById(R.id.rgJenisTelepon);
        tombolTampil = findViewById(R.id.btnTampilkan);

        tombolTampil.setOnClickListener(v -> prosesInput());
    }

    private void prosesInput() {
        String nomor = inputTelepon.getText().toString().trim();

        if (nomor.isEmpty()) {
            Toast.makeText(this, "Nomor telepon belum diisi", Toast.LENGTH_SHORT).show();
            return;
        }

        int idTerpilih = grupPilihan.getCheckedRadioButtonId();
        if (idTerpilih == -1) {
            Toast.makeText(this, "Pilih jenis telepon dulu", Toast.LENGTH_SHORT).show();
            return;
        }

        RadioButton radioAktif = findViewById(idTerpilih);
        String jenis = radioAktif.getText().toString();

        String pesan = jenis + ": " + nomor;
        Toast.makeText(this, pesan, Toast.LENGTH_LONG).show();
    }
}