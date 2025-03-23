namespace Bai2Tuan5
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
            this.txt_TenKhoa = new System.Windows.Forms.TextBox();
            this.dgr_SV = new System.Windows.Forms.DataGridView();
            this.label4 = new System.Windows.Forms.Label();
            this.txt_TongSV = new System.Windows.Forms.TextBox();
            this.btn_Thoat = new System.Windows.Forms.Button();
            this.cbb_MaKhoa = new System.Windows.Forms.ComboBox();
            this.col_MaSV = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.col_HoSV = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.col_TenSV = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.col_NgaySinh = new System.Windows.Forms.DataGridViewTextBoxColumn();
            ((System.ComponentModel.ISupportInitialize)(this.dgr_SV)).BeginInit();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.ForeColor = System.Drawing.Color.Red;
            this.label1.Location = new System.Drawing.Point(77, 54);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(409, 25);
            this.label1.TabIndex = 0;
            this.label1.Text = "THỐNG KÊ SỐ SINH VIÊN THEO KHOA";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(14, 131);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(62, 16);
            this.label2.TabIndex = 1;
            this.label2.Text = "Mã khoa:";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(242, 131);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(67, 16);
            this.label3.TabIndex = 2;
            this.label3.Text = "Tên khoa:";
            // 
            // txt_TenKhoa
            // 
            this.txt_TenKhoa.Location = new System.Drawing.Point(315, 128);
            this.txt_TenKhoa.Name = "txt_TenKhoa";
            this.txt_TenKhoa.Size = new System.Drawing.Size(197, 22);
            this.txt_TenKhoa.TabIndex = 4;
            // 
            // dgr_SV
            // 
            this.dgr_SV.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dgr_SV.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.col_MaSV,
            this.col_HoSV,
            this.col_TenSV,
            this.col_NgaySinh});
            this.dgr_SV.Location = new System.Drawing.Point(12, 166);
            this.dgr_SV.Name = "dgr_SV";
            this.dgr_SV.RowHeadersWidth = 51;
            this.dgr_SV.RowTemplate.Height = 24;
            this.dgr_SV.Size = new System.Drawing.Size(578, 185);
            this.dgr_SV.TabIndex = 5;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(99, 381);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(115, 16);
            this.label4.TabIndex = 6;
            this.label4.Text = "Tổng số sinh viên:";
            // 
            // txt_TongSV
            // 
            this.txt_TongSV.Location = new System.Drawing.Point(220, 378);
            this.txt_TongSV.Name = "txt_TongSV";
            this.txt_TongSV.ReadOnly = true;
            this.txt_TongSV.Size = new System.Drawing.Size(128, 22);
            this.txt_TongSV.TabIndex = 7;
            // 
            // btn_Thoat
            // 
            this.btn_Thoat.Location = new System.Drawing.Point(368, 374);
            this.btn_Thoat.Name = "btn_Thoat";
            this.btn_Thoat.Size = new System.Drawing.Size(86, 30);
            this.btn_Thoat.TabIndex = 8;
            this.btn_Thoat.Text = "Thoát";
            this.btn_Thoat.UseVisualStyleBackColor = true;
            this.btn_Thoat.Click += new System.EventHandler(this.btn_Thoat_Click);
            // 
            // cbb_MaKhoa
            // 
            this.cbb_MaKhoa.FormattingEnabled = true;
            this.cbb_MaKhoa.Items.AddRange(new object[] {
            "kt",
            "tc",
            "th",
            "xd",
            "xh"});
            this.cbb_MaKhoa.Location = new System.Drawing.Point(82, 126);
            this.cbb_MaKhoa.Name = "cbb_MaKhoa";
            this.cbb_MaKhoa.Size = new System.Drawing.Size(121, 24);
            this.cbb_MaKhoa.TabIndex = 9;
            this.cbb_MaKhoa.SelectedIndexChanged += new System.EventHandler(this.cbb_MaKhoa_SelectedIndexChanged);
            // 
            // col_MaSV
            // 
            this.col_MaSV.DataPropertyName = "MaSV";
            this.col_MaSV.HeaderText = "Mã SV";
            this.col_MaSV.MinimumWidth = 6;
            this.col_MaSV.Name = "col_MaSV";
            this.col_MaSV.Width = 125;
            // 
            // col_HoSV
            // 
            this.col_HoSV.DataPropertyName = "HoSV";
            this.col_HoSV.HeaderText = "Họ SV";
            this.col_HoSV.MinimumWidth = 6;
            this.col_HoSV.Name = "col_HoSV";
            this.col_HoSV.Width = 125;
            // 
            // col_TenSV
            // 
            this.col_TenSV.DataPropertyName = "TenSV";
            this.col_TenSV.HeaderText = "Tên SV";
            this.col_TenSV.MinimumWidth = 6;
            this.col_TenSV.Name = "col_TenSV";
            this.col_TenSV.Width = 125;
            // 
            // col_NgaySinh
            // 
            this.col_NgaySinh.DataPropertyName = "NgaySinh";
            this.col_NgaySinh.HeaderText = "Ngày sinh";
            this.col_NgaySinh.MinimumWidth = 6;
            this.col_NgaySinh.Name = "col_NgaySinh";
            this.col_NgaySinh.Width = 125;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(601, 425);
            this.Controls.Add(this.cbb_MaKhoa);
            this.Controls.Add(this.btn_Thoat);
            this.Controls.Add(this.txt_TongSV);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.dgr_SV);
            this.Controls.Add(this.txt_TenKhoa);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Name = "Form1";
            this.Text = "Thống kê sinh viên theo khoa";
            this.Load += new System.EventHandler(this.Form1_Load);
            ((System.ComponentModel.ISupportInitialize)(this.dgr_SV)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox txt_TenKhoa;
        private System.Windows.Forms.DataGridView dgr_SV;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox txt_TongSV;
        private System.Windows.Forms.Button btn_Thoat;
        private System.Windows.Forms.ComboBox cbb_MaKhoa;
        private System.Windows.Forms.DataGridViewTextBoxColumn col_MaSV;
        private System.Windows.Forms.DataGridViewTextBoxColumn col_HoSV;
        private System.Windows.Forms.DataGridViewTextBoxColumn col_TenSV;
        private System.Windows.Forms.DataGridViewTextBoxColumn col_NgaySinh;
    }
}

