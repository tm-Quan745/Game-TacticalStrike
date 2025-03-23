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

namespace Bai4Tuan5
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
            LoadDuLieu();
            txt_TongKhoa.Text = (dgr_Khoa.Rows.Count-1).ToString();
            btn_Luu.Enabled = false;
            btn_Huy.Enabled = false;
        }

        public void LoadDuLieu()
        {
            string sql = "select * from QLKhoa";
            dgr_Khoa.DataSource = kn.TaoBang(sql);
            txt_TongKhoa.Text = (dgr_Khoa.Rows.Count - 1).ToString();

        }
        private void dgr_Khoa_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            int chiso = -1;
            DataTable bang = (DataTable)dgr_Khoa.DataSource;
            chiso = dgr_Khoa.SelectedCells[0].RowIndex;
            DataRow hang = bang.Rows[chiso];

            txt_MaKhoa.Text = hang["MaKhoa"].ToString().Trim();
            txt_TenKhoa.Text = hang["TenKhoa"].ToString().Trim();

        }

        private void btn_Thoat_Click(object sender, EventArgs e)
        {
            this.Close();
            kn.myDisconnect();
        }

        private void btn_Them_Click(object sender, EventArgs e)
        {
            txt_MaKhoa.ResetText();
            txt_TenKhoa.ResetText();
            txt_MaKhoa.Focus();

            this.btn_Huy.Enabled = true;
            this.btn_Luu.Enabled = true;
            this.btn_Them.Enabled = false;
        }

        private void btn_Sua_Click(object sender, EventArgs e)
        {
            string sql = "select * from QLKhoa where MaKhoa='" + txt_MaKhoa.Text + "'";
            DataTable dt = new DataTable();
            dt = kn.TaoBang(sql);
            if (dt.Rows.Count != 0)
            {
                kn.sua(txt_MaKhoa.Text, txt_TenKhoa.Text);
            }
            else
                MessageBox.Show("Bạn chưa chọn dữ liệu để sửa", "Thông Báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
            txt_MaKhoa.ResetText();
            txt_TenKhoa.ResetText();
            txt_MaKhoa.Focus();
            LoadDuLieu();
        }

        private void btn_Xoa_Click(object sender, EventArgs e)
        {
            string sql = "select * from QLKhoa where MaKhoa='"+txt_MaKhoa.Text+"'";
            DataTable dt = new DataTable();
            dt = kn.TaoBang(sql);
            if(dt.Rows.Count != 0)
            {
                kn.xoa(txt_MaKhoa.Text,txt_TenKhoa.Text);
            }
            else
            {
                MessageBox.Show("Bạn chưa chọn dữ liệu để xoá", "Thông Báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            txt_MaKhoa.ResetText();
            txt_TenKhoa.ResetText();
            txt_MaKhoa.Focus();
            LoadDuLieu();
        }

        private void btn_Huy_Click(object sender, EventArgs e)
        {
            txt_MaKhoa.ResetText();
            txt_TenKhoa.ResetText();
            txt_MaKhoa.Focus();

            this.btn_Them.Enabled = true;
        }

        private void btn_Luu_Click(object sender, EventArgs e)
        {
            string sql = "select * from QLKhoa where MaKhoa='" + txt_MaKhoa.Text + "'";
            DataTable dt = new DataTable();
            dt = kn.TaoBang(sql);
            if(dt.Rows.Count == 0)
            {
                kn.them(txt_MaKhoa.Text ,txt_TenKhoa.Text);

                txt_MaKhoa.ResetText();
                txt_TenKhoa.ResetText();
                txt_MaKhoa.Focus();
            }
            else
                MessageBox.Show("Mã số khoa đã có sẵn vui lòng nhập lại","Thông Báo",MessageBoxButtons.OK,MessageBoxIcon.Information);

            this.btn_Huy.Enabled = true;
            this.btn_Luu.Enabled = false;
            this.btn_Them.Enabled = true;
            LoadDuLieu();
        }
    }
    public class KetNoiDuLieu
    {
        SqlConnection conn = new SqlConnection("Data Source=.;Initial Catalog=QuanLiSinhVien;Integrated Security=True;Encrypt=True;" +
            "TrustServerCertificate=True");
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
            SqlDataAdapter ds = new SqlDataAdapter(sql, conn);
            ds.Fill(dt);
            return dt;

        }
        public void them(string ma, string ten)
        {
            string sql = "insert into QLKhoa(MaKhoa,TenKhoa)" + "values('" + ma + "',N'" + ten + "')";
            SqlCommand cmd = new SqlCommand(sql, conn);
            cmd.ExecuteNonQuery();
        }
        public void xoa(string ma, string ten)
        {
            string sql = "delete from QLKhoa where MaKhoa='" + ma + "'";
            SqlCommand c = new SqlCommand(sql, conn);
            c.ExecuteNonQuery();
        }
        public void sua(string ma, string ten)
        {
            try
            {
                string sql = "UPDATE QLKhoa SET TenKhoa = @TenKhoa WHERE MaKhoa = @MaKhoa";
                SqlCommand s = new SqlCommand(sql, conn);
                s.Parameters.AddWithValue("@MaKhoa", ma.Trim());
                s.Parameters.AddWithValue("@TenKhoa", ten.Trim());

                int rowsAffected = s.ExecuteNonQuery(); // Kiểm tra số dòng bị ảnh hưởng
                if (rowsAffected > 0)
                    MessageBox.Show("Cập nhật thành công!", "Thông Báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
                else
                    MessageBox.Show("Không có dữ liệu nào được cập nhật!", "Thông Báo", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Lỗi khi cập nhật: " + ex.Message, "Lỗi", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

    }

}
