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

namespace Bai5Tuan5
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        KetNoiDuLieu kn = new KetNoiDuLieu();

        public void LoadData()
        {
            string sql = "select * from QLNV";
            dgr_NV.DataSource = kn.TaoBang(sql);
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            kn.myconnect();
            LoadData();
            string query = "SELECT MaPB, TenPB FROM QLPB";
            DataTable dt = kn.TaoBang(query);

            lb_DSPB.DataSource = dt;
            lb_DSPB.DisplayMember = "TenPB";
            lb_DSPB.ValueMember = "MaPB";
            txt_MaPB.Text = lb_DSPB.SelectedValue.ToString().Trim();
            this.btn_ChapNhan.Enabled = false;
            this.btn_Huy.Enabled = false;

        }

        private void dgr_NV_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            int chiso = -1;
            DataTable bang = new DataTable();
            bang = (DataTable)dgr_NV.DataSource;
            chiso = dgr_NV.SelectedCells[0].RowIndex;
            DataRow hang = bang.Rows[chiso];

            txt_MaNV.Text = hang["MaNV"].ToString().Trim();
            txt_TenNV.Text = hang["TenNV"].ToString().Trim();
            dt_NgaySinh.Value = Convert.ToDateTime(hang["ngaysinh"].ToString());
            txt_SDT.Text = hang["SoDT"].ToString().Trim(); 
            txt_MaPB.Text = hang["MaPB"].ToString().Trim();
        }

        private void btn_Them_Click(object sender, EventArgs e)
        {
            txt_MaNV.ResetText();
            txt_TenNV.ResetText();
            dt_NgaySinh.ResetText();
            txt_SDT.ResetText();
            txt_MaPB.ResetText();
            txt_MaNV.Focus();

            this.btn_ChapNhan.Enabled = true;
            this.btn_Huy.Enabled = true;
            this.btn_Them.Enabled = false;
            LoadData();
        }

        private void btn_ChapNhan_Click(object sender, EventArgs e)
        {
            string sql = "select * from QLNV where MaNV='"+txt_MaNV.Text+"'";
            DataTable dt = kn.TaoBang(sql);
            if (dt.Rows.Count > 0)
            {
                MessageBox.Show("Mã nhân viên đã tồn tại","Thông Báo");
                txt_MaNV.ResetText();
                txt_MaNV.Focus();
            }
            else
            {
                kn.them(txt_MaNV.Text, txt_TenNV.Text, txt_SDT.Text, dt_NgaySinh.Value.ToString("yyyy/MM/dd"), txt_MaPB.Text);
                this.btn_ChapNhan.Enabled = false;
                this.btn_Huy.Enabled = true;
                LoadData();
            }
        }

        private void btn_Huy_Click(object sender, EventArgs e)
        {
            txt_MaNV.ResetText();
            txt_TenNV.ResetText();
            dt_NgaySinh.ResetText();
            txt_SDT.ResetText();
            txt_MaPB.ResetText();
            txt_MaNV.Focus();

            this.btn_Them.Enabled = true;
            LoadData();
        }

        private void btn_Sua_Click(object sender, EventArgs e)
        {
            string sql = "select * from QLNV where MaNV='" + txt_MaNV.Text + "'";
            DataTable dt = kn.TaoBang(sql);
            if (dt.Rows.Count == 0)
            {
                MessageBox.Show("Bạn chưa chọn mã nhân viên để sửa", "Thông Báo",MessageBoxButtons.OK,MessageBoxIcon.Information);
            }
            else
            {
                kn.sua(txt_MaNV.Text, txt_TenNV.Text, txt_SDT.Text, dt_NgaySinh.Value.ToString("yyyy/MM/dd"), txt_MaPB.Text);
                LoadData();
            }
        }

        private void btn_Xoa_Click(object sender, EventArgs e)
        {
            string sql = "select * from QLNV where MaNV='" + txt_MaNV.Text + "'";
            DataTable dt = kn.TaoBang(sql);
            if (dt.Rows.Count == 0)
            {
                MessageBox.Show("Bạn chưa chọn mã nhân viên để xóa", "Thông Báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                kn.xoa(txt_MaNV.Text);
                LoadData();
            }
        }

        private void lb_DSPB_SelectedIndexChanged(object sender, EventArgs e)
        {
           if (lb_DSPB.SelectedValue != null)
            {
                txt_MaPB.Text = lb_DSPB.SelectedValue.ToString().Trim();
            }
        }

        private void txt_MaPB_TextChanged(object sender, EventArgs e)
        {
            bool found = false; // Biến kiểm tra xem có tìm thấy mã phòng không
            for (int i = 0; i < lb_DSPB.Items.Count; i++)
            {
                DataRowView row = lb_DSPB.Items[i] as DataRowView; // Chuyển từng item về DataRowView
                if (row != null && row["MaPB"].ToString().Trim() == txt_MaPB.Text.Trim())
                {
                    lb_DSPB.SelectedIndex = i; // Chọn item có MaPhong tương ứng
                    found = true;
                    break;
                }
            }

            if (!found)
            {
                lb_DSPB.SelectedIndex = -1; // Nếu không tìm thấy, bỏ chọn
            }
        }
    }
    }
    public class KetNoiDuLieu
    {
        SqlConnection conn = new SqlConnection("Data Source=.;Initial Catalog=Quanlinhanvien;Integrated Security=True;" +
            "TrustServerCertificate=True");
        public void myconnect()
        {
            conn.Open();
        }
        public void myclose()
        {
            conn.Close();
        }
        public DataTable TaoBang(string sql)
        {
            SqlDataAdapter adap = new SqlDataAdapter(sql, conn);
            DataTable bang = new DataTable();
            adap.Fill(bang);
            return bang;
        }
        public void them(string ma,string ten,string sdt,string NgaySinh,string maPB)
        {
            string sql = "insert into QLNV values('" + ma + "',N'" + ten + "','" + NgaySinh + "','" + sdt + "','"+maPB+"')";
            SqlCommand cmd = new SqlCommand(sql, conn);
            cmd.ExecuteNonQuery();
        }
        public void sua(string ma, string ten, string sdt, string NgaySinh, string maPB)
        {
            string sql = "update QLNV set TenNV=N'" + ten + "',NgaySinh='" + NgaySinh + "',MaPB='" + maPB + "' where MaNV='" + ma + "'";
            SqlCommand cmd = new SqlCommand(sql, conn);
            cmd.ExecuteNonQuery();
        }
        public void xoa(string ma)
        {
            string sql = "delete from QLNV where MaNV='" + ma + "'";
            SqlCommand cmd = new SqlCommand(sql, conn);
            cmd.ExecuteNonQuery();
        }
    }
    
