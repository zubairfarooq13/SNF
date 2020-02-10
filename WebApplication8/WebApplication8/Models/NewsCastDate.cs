using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace WebApplication8.Models
{
    public class NewsCastDate
    {
        public int news_id { get; set; }
        public DateTime date { get; set; }
        public string heading { get; set; }
        public string content { get; set; }
        public Nullable<int> id_authors { get; set; }
        public Nullable<int> id_categories { get; set; }
        public Nullable<int> id_web { get; set; }

    }
}