using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace WebApplication8.Models
{
    public class NewsDataViewModel
    {
        public news_detail News_Detail { get; set; }
        public author Author { get; set; }
        public web_name Source { get; set; }
        public category Category { get; set; }


    }
}