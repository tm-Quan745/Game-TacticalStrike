using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Bai3Tuan5
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        KetNoiDuLieu kn = new KetNoiDuLieu();
        private void Form1_Load(object sender, EventArgs e)
        {
            kn.myConnect();
            string sql = "select * from QLSV";
            cb_MaSV.DataSource = kn.TaoBang(sql);
            cb_MaSV.DisplayMember = "MaSV";
            btn_Tim.Focus();

        }
        private void btn_Thoat_Click(object sender, EventArgs e)
        {
            this.Close();
            kn.myDisconnect();
        }

        private void cb_MaSV_SelectedIndexChanged(object sender, EventArgs e)
        {
            
        }

        private void btn_Tim_Click(object sender, EventArgs e)
        {
            string sql = "SELECT * FROM QLSV WHERE MaSV='" + cb_MaSV.Text +"'";
            SqlCommand cmd = new SqlCommand(sql);
            cmd.Parameters.AddWithValue("@MaSV", cb_MaSV.Text);
            DataTable d = kn.TaoBang(sql);
            if (d.Rows.Count == 0)
            {
                MessageBox.Show("Không tìm thấy sinh viên!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
                return; // Thoát khỏi hàm, không chạy tiếp
            }
            else
            {
                foreach (DataRow hang in d.Rows)
                {

                    txt_HoTen.Text = hang["HoSV"].ToString().Trim() + " " + hang["TenSV"].ToString().Trim();
                    txt_GioiTinh.Text = hang["GioiTinh"].ToString().Trim();
                    txt_MaKhoa.Text = hang["MaKhoa"].ToString().Trim();
                    dt_NgaySinh.Value = Convert.ToDateTime(hang["NgaySinh"]);
                }
                string sql1 = "SELECT MaMH,TenMH,DiemThi FROM QLMH WHERE MaSV='" + cb_MaSV.Text+ "'";
                dgr_SV.DataSource = kn.TaoBang(sql1);
            }
            
        }

    }
    public class KetNoiDuLieu
    {
        SqlConnection conn = new SqlConnection("Data Source=.;Initial Catalog=QuanLiSinhVien;Integrated Security=True;" +
            "Encrypt=True;TrustServerCertificate=True");
        public void myConnect()
        {
            conn.Open();
        }
        public void myDisconnect()
        {
            conn.Close();
        }
        public DataTable TaoBang(string sql)
        {
            DataTable dt = new DataTable();
            SqlDataAdapter ds = new SqlDataAdapter(sql,conn);
            ds.Fill(dt);
            return dt;
        }
    }
}
