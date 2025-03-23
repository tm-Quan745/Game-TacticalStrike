namespace Bai3Tuan5
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.txt_GioiTinh = new System.Windows.Forms.TextBox();
            this.txt_HoTen = new System.Windows.Forms.TextBox();
            this.txt_MaKhoa = new System.Windows.Forms.TextBox();
            this.btn_Tim = new System.Windows.Forms.Button();
            this.btn_Thoat = new System.Windows.Forms.Button();
            this.cb_MaSV = new System.Windows.Forms.ComboBox();
            this.dt_NgaySinh = new System.Windows.Forms.DateTimePicker();
            this.dgr_SV = new System.Windows.Forms.DataGridView();
            this.col_MaMH = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.col_TenMH = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.col_DiemThi = new System.Windows.Forms.DataGridViewTextBoxColumn();
            ((System.ComponentModel.ISupportInitialize)(this.dgr_SV)).BeginInit();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft YaHei", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.ForeColor = System.Drawing.Color.Red;
            this.label1.Location = new System.Drawing.Point(111, 37);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(354, 27);
            this.label1.TabIndex = 0;
            this.label1.Text = "TÌM KIẾM THÔNG TIN SINH VIÊN";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(21, 98);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(86, 16);
            this.label2.TabIndex = 1;
            this.label2.Text = "Nhập mã SV:";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(21, 149);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(70, 16);
            this.label3.TabIndex = 2;
            this.label3.Text = "Ngày sinh:";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(308, 101);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(70, 16);
            this.label4.TabIndex = 3;
            this.label4.Text = "Họ tên SV:";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(308, 149);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(62, 16);
            this.label5.TabIndex = 4;
            this.label5.Text = "Mã khoa:";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(21, 198);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(57, 16);
            this.label6.TabIndex = 5;
            this.label6.Text = "Giới tính:";
            // 
            // txt_GioiTinh
            // 
            this.txt_GioiTinh.Location = new System.Drawing.Point(116, 192);
            this.txt_GioiTinh.Name = "txt_GioiTinh";
            this.txt_GioiTinh.ReadOnly = true;
            this.txt_GioiTinh.Size = new System.Drawing.Size(136, 22);
            this.txt_GioiTinh.TabIndex = 7;
            // 
            // txt_HoTen
            // 
            this.txt_HoTen.Location = new System.Drawing.Point(384, 92);
            this.txt_HoTen.Name = "txt_HoTen";
            this.txt_HoTen.ReadOnly = true;
            this.txt_HoTen.Size = new System.Drawing.Size(225, 22);
            this.txt_HoTen.TabIndex = 8;
            // 
            // txt_MaKhoa
            // 
            this.txt_MaKhoa.Location = new System.Drawing.Point(384, 143);
            this.txt_MaKhoa.Name = "txt_MaKhoa";
            this.txt_MaKhoa.ReadOnly = true;
            this.txt_MaKhoa.Size = new System.Drawing.Size(136, 22);
            this.txt_MaKhoa.TabIndex = 9;
            // 
            // btn_Tim
            // 
            this.btn_Tim.Location = new System.Drawing.Point(383, 188);
            this.btn_Tim.Name = "btn_Tim";
            this.btn_Tim.Size = new System.Drawing.Size(115, 33);
            this.btn_Tim.TabIndex = 10;
            this.btn_Tim.Text = "Tìm";
            this.btn_Tim.UseVisualStyleBackColor = true;
            this.btn_Tim.Click += new System.EventHandler(this.btn_Tim_Click);
            // 
            // btn_Thoat
            // 
            this.btn_Thoat.Location = new System.Drawing.Point(501, 188);
            this.btn_Thoat.Name = "btn_Thoat";
            this.btn_Thoat.Size = new System.Drawing.Size(115, 33);
            this.btn_Thoat.TabIndex = 11;
            this.btn_Thoat.Text = "Thoát";
            this.btn_Thoat.UseVisualStyleBackColor = true;
            this.btn_Thoat.Click += new System.EventHandler(this.btn_Thoat_Click);
            // 
            // cb_MaSV
            // 
            this.cb_MaSV.FormattingEnabled = true;
            this.cb_MaSV.Items.AddRange(new object[] {
            "sv1",
            "sv2",
            "sv3",
            "sv4"});
            this.cb_MaSV.Location = new System.Drawing.Point(116, 90);
            this.cb_MaSV.Name = "cb_MaSV";
            this.cb_MaSV.Size = new System.Drawing.Size(161, 24);
            this.cb_MaSV.TabIndex = 12;
            this.cb_MaSV.SelectedIndexChanged += new System.EventHandler(this.cb_MaSV_SelectedIndexChanged);
            // 
            // dt_NgaySinh
            // 
            this.dt_NgaySinh.CustomFormat = "dd/MM/yyyy";
            this.dt_NgaySinh.Format = System.Windows.Forms.DateTimePickerFormat.Custom;
            this.dt_NgaySinh.Location = new System.Drawing.Point(116, 144);
            this.dt_NgaySinh.Name = "dt_NgaySinh";
            this.dt_NgaySinh.Size = new System.Drawing.Size(161, 22);
            this.dt_NgaySinh.TabIndex = 13;
            // 
            // dgr_SV
            // 
            this.dgr_SV.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dgr_SV.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.col_MaMH,
            this.col_TenMH,
            this.col_DiemThi});
            this.dgr_SV.Location = new System.Drawing.Point(24, 236);
            this.dgr_SV.Name = "dgr_SV";
            this.dgr_SV.RowHeadersWidth = 51;
            this.dgr_SV.RowTemplate.Height = 24;
            this.dgr_SV.Size = new System.Drawing.Size(592, 150);
            this.dgr_SV.TabIndex = 14;
            // 
            // col_MaMH
            // 
            this.col_MaMH.DataPropertyName = "MaMH";
            this.col_MaMH.HeaderText = "Mã môn học";
            this.col_MaMH.MinimumWidth = 6;
            this.col_MaMH.Name = "col_MaMH";
            this.col_MaMH.Width = 125;
            // 
            // col_TenMH
            // 
            this.col_TenMH.DataPropertyName = "TenMH";
            this.col_TenMH.HeaderText = "Tên Môn học";
            this.col_TenMH.MinimumWidth = 6;
            this.col_TenMH.Name = "col_TenMH";
            this.col_TenMH.Width = 125;
            // 
            // col_DiemThi
            // 
            this.col_DiemThi.DataPropertyName = "DiemThi";
            this.col_DiemThi.HeaderText = "Điểm thi";
            this.col_DiemThi.MinimumWidth = 6;
            this.col_DiemThi.Name = "col_DiemThi";
            this.col_DiemThi.Width = 125;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(630, 432);
            this.Controls.Add(this.dgr_SV);
            this.Controls.Add(this.dt_NgaySinh);
            this.Controls.Add(this.cb_MaSV);
            this.Controls.Add(this.btn_Thoat);
            this.Controls.Add(this.btn_Tim);
            this.Controls.Add(this.txt_MaKhoa);
            this.Controls.Add(this.txt_HoTen);
            this.Controls.Add(this.txt_GioiTinh);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Name = "Form1";
            this.Text = "Tìm kiếm thông tin sinh viên";
            this.Load += new System.EventHandler(this.Form1_Load);
            ((System.ComponentModel.ISupportInitialize)(this.dgr_SV)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.TextBox txt_GioiTinh;
        private System.Windows.Forms.TextBox txt_HoTen;
        private System.Windows.Forms.TextBox txt_MaKhoa;
        private System.Windows.Forms.Button btn_Tim;
        private System.Windows.Forms.Button btn_Thoat;
        private System.Windows.Forms.ComboBox cb_MaSV;
        private System.Windows.Forms.DateTimePicker dt_NgaySinh;
        private System.Windows.Forms.DataGridView dgr_SV;
        private System.Windows.Forms.DataGridViewTextBoxColumn col_MaMH;
        private System.Windows.Forms.DataGridViewTextBoxColumn col_TenMH;
        private System.Windows.Forms.DataGridViewTextBoxColumn col_DiemThi;
    }
}

