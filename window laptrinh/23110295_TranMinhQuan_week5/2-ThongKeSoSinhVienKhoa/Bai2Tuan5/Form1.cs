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

namespace Bai2Tuan5
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        KetNoiDuLieu kn = new KetNoiDuLieu();

        private void btn_Thoat_Click(object sender, EventArgs e)
        {
            this.Close();
            kn.Mydisconnect();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            kn.Myconnect();
            string sql = "SELECT * FROM QLKhoa";
            cbb_MaKhoa.DataSource = kn.TaoBang(sql);
            cbb_MaKhoa.DisplayMember = "MaKhoa";
        }

        private void cbb_MaKhoa_SelectedIndexChanged(object sender, EventArgs e)
        {
            string sql = "SELECT * FROM QLKhoa WHERE MaKhoa = '" + cbb_MaKhoa.Text + "'";
            DataTable dt = kn.TaoBang(sql);
            foreach (DataRow hang in dt.Rows)
                txt_TenKhoa.Text = hang["TenKhoa"].ToString();
            string sql1 = "SELECT MaSV,HoSV,TenSV,NgaySinh From QLSV " +
                "sv,QLKhoa kh where (sv.MaKhoa=kh.MaKhoa) and (kh.MaKhoa='" + cbb_MaKhoa.Text + "')";
            dgr_SV.DataSource = kn.TaoBang(sql1);
            string sql2 = "SELECT COUNT(MaKhoa) FROM QLSV where MaKhoa='\" + cbMaKhoa.Text + \"' group by MaKhoa";
            txt_TongSV.Text = (dgr_SV.Rows.Count - 1).ToString();
        }
    }
    public class KetNoiDuLieu
    {
        SqlConnection conn = new SqlConnection("Data Source=.;Initial Catalog=QuanLiSinhVien;Integrated Security=True;Encrypt=True;" +
            "TrustServerCertificate=True");
        public void Myconnect()
        {
            conn.Open();
        }
        public void Mydisconnect()
        {
            conn.Close();
        }
        public DataTable TaoBang(string sql)
        {
            DataTable dt = new DataTable();
            SqlDataAdapter ds = new SqlDataAdapter(sql,conn);
            ds.Fill(dt);
            return (dt);
        }
    }
}
