using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace WebApplication8.Models
{
    public class FilterDateOrCheck
    {
        public string ToDate { get; set; }
        public string FromDate { get; set; }
        public bool DawnNews { get; set; }
        public bool PakistanToday { get; set; }

    }
}