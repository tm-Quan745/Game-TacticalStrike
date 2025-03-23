using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.Common;
using System.Data.SqlClient;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Bai1Tuan5
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        KetNoiDL kn = new KetNoiDL();


        private void btn_Thoat_Click(object sender, EventArgs e)
        {
            this.Close();
            kn.MyDisconnec();
        }
        private void LoadDuLieu()
        {
            string sql = "select * from QLSV";
            dGr_SV.DataSource = kn.TaoBang(sql);
        }

        private void dGr_SV_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            int chiso = -1;
            DataTable bang = new DataTable();
            bang = (DataTable)dGr_SV.DataSource;
            chiso = dGr_SV.SelectedCells[0].RowIndex;
            DataRow hang = bang.Rows[chiso];

            txt_MaSV.Text = hang["masv"].ToString().Trim();
            txt_HoSV.Text = hang["hosv"].ToString().Trim();
            txt_TenSV.Text = hang["tensv"].ToString().Trim();
            txt_MaKhoa.Text = hang["makhoa"].ToString().Trim();
            txt_GioiTinh.Text = hang["gioitinh"].ToString().Trim();
            dt_NgaySinh.Value = Convert.ToDateTime(hang["ngaysinh"].ToString());
        }

        private void btn_Them_Click(object sender, EventArgs e)
        {
            txt_MaSV.ResetText();
            txt_HoSV.ResetText();
            txt_TenSV.ResetText();
            txt_MaKhoa.ResetText();
            txt_GioiTinh.ResetText();
            dt_NgaySinh.Value = DateTime.Now;
            txt_MaSV.Focus();
            this.btn_Luu.Enabled = true;
            this.btn_Huy.Enabled = true;
            this.btn_Them.Enabled = false;
            LoadDuLieu();

        }
        private void btn_Luu_Click(object sender, EventArgs e)
        {
            this.btn_Them.Enabled = true;
            this.btn_Luu.Enabled = false;
            this.btn_Huy.Enabled = false;
            string sql = "select * from QLSV where MaSV = '" + txt_MaSV.Text + "'";
            DataTable dt = new DataTable();
            dt = kn.TaoBang(sql);
            if (dt.Rows.Count == 0)
            {
                kn.them(txt_MaSV.Text, txt_HoSV.Text, txt_TenSV.Text, dt_NgaySinh.Value, 
                    txt_GioiTinh.Text, txt_MaKhoa.Text);
                txt_MaSV.ResetText();
                txt_HoSV.ResetText();
                txt_TenSV.ResetText();
                txt_MaKhoa.ResetText();
                txt_GioiTinh.ResetText();
                dt_NgaySinh.ResetText();
                txt_MaSV.Focus();
            }
            else
            {
                MessageBox.Show("Mã sinh viên đã tồn tại", "Thông Báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            LoadDuLieu();
        }
        private void btn_Xoa_Click(object sender, EventArgs e)
        {
            string s = "SELECT * FROM QLSV where MaSV='" + txt_MaSV.Text + "'";
            DataTable dt = new DataTable();
            dt = kn.TaoBang(s);
            if (dt.Rows.Count != 0)
            {
                kn.xoa(txt_MaSV.Text, txt_HoSV.Text, txt_TenSV.Text, dt_NgaySinh.Value, txt_GioiTinh.Text, txt_MaKhoa.Text);

                txt_GioiTinh.ResetText();
                txt_HoSV.ResetText();
                txt_MaKhoa.ResetText();
                txt_MaSV.ResetText();
                dt_NgaySinh.ResetText();
                txt_TenSV.ResetText();
                txt_MaSV.Focus();
            }
            else
            {
                MessageBox.Show("Bạn chưa chọn dữ liệu để xoá", "Thông Báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            LoadDuLieu();
        }

        private void btn_Sua_Click(object sender, EventArgs e)
        {
            string s = "SELECT * FROM QLSV where MaSV='" + txt_MaSV.Text + "'";
            DataTable dt = new DataTable();
            dt = kn.TaoBang(s);
            if (dt.Rows.Count != 0)
            {
                kn.sua(txt_MaSV.Text, txt_HoSV.Text, txt_TenSV.Text, dt_NgaySinh.Value, txt_GioiTinh.Text, txt_MaKhoa.Text);
            }
            else
            {
                MessageBox.Show("Bạn chưa chọn dữ liệu để sửa", "Thông Báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            LoadDuLieu();

        }

        private void btn_Huy_Click(object sender, EventArgs e)
        {
            txt_GioiTinh.ResetText();
            txt_HoSV.ResetText();
            txt_MaKhoa.ResetText();
            txt_MaSV.ResetText();
            dt_NgaySinh.ResetText();
            txt_TenSV.ResetText();
            txt_MaSV.Focus();

            this.btn_Them.Enabled = true;
            LoadDuLieu();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            kn.MyConnec();
            LoadDuLieu();
            this.btn_Huy.Enabled = false;
            this.btn_Luu.Enabled = false;
        }
    }
    public class KetNoiDL
    {
        public SqlConnection cnn = new SqlConnection("Data Source=.;Initial Catalog=QuanLiSinhVien;Integrated Security=True");
        public void MyConnec()
        {
            cnn.Open();
        }
        public void MyDisconnec()
        {
            cnn.Close();
        }
        public DataTable TaoBang(string sql)
        {
            DataTable dt = new DataTable();
            SqlDataAdapter ds = new SqlDataAdapter(sql, cnn);
            ds.Fill(dt);
            return dt;
        }
        public void them(string ma, string ho, string ten, DateTime ngaysinh,
                        string gioitinh, string maKhoa)
        {
            if (cnn.State == ConnectionState.Closed)
            {
                MyConnec();
            }
            string sql = "insert into QLSV(MaSV,HoSV,TenSV,NgaySinh,GioiTinh,MaKhoa) " +
                "values('" + ma + "',N'" + ho + "',N'" + ten + "','" + ngaysinh.ToString("yyyy-MM-dd") + "',N'" + gioitinh + "','" + maKhoa + "')";
            SqlCommand cmd = new SqlCommand(sql, cnn);
            cmd.ExecuteNonQuery();
        }
        public void xoa(string ma, string ho, string ten, DateTime ngaysinh,
                        string gioitinh, string maKhoa)
        {
            string sql = "delete from QLSV where MaSV='" + ma + "'";
            SqlCommand cmd = new SqlCommand(sql, cnn);
            cmd.ExecuteNonQuery();
        }
        public void sua(string ma, string ho, string ten, DateTime ngaysinh,
                        string gioitinh, string maKhoa)
        {
            if (cnn.State == ConnectionState.Closed)
            {
                MyConnec();
            }
            string sql = "update QLSV set HoSV=N'" + ho + "',TenSV=N'" + ten + "',NgaySinh='" + ngaysinh.ToString("yyyy-MM-dd") + "',GioiTinh=N'" + gioitinh + "',MaKhoa='" + maKhoa + "' where MaSV='" + ma + "'";
            SqlCommand cmd = new SqlCommand(sql, cnn);
            cmd.ExecuteNonQuery();
        }
    }
    

    }




