using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using WebApplication8.Models;

namespace WebApplication8.Controllers
{
    //visual studio dobara kiya ha.nii you need to install ado.net component then it would be visible
    // update visual studio and add it when install setup of visual studio
    public class HomeController : Controller
    {
        private readonly web_dataEntities _dbContext;
        public HomeController()
        {
            _dbContext = new web_dataEntities();
        }
        //please update model1.edmx, idea ni update kerny ka, shyd command likhni prti ha?nahi 
        public ActionResult Index()
        {   
            var authors = _dbContext.authors.ToList();
            var webNames = _dbContext.web_name.ToList();
            List<NewsDataViewModel> newsDetailList = new List<NewsDataViewModel>();
            var newsList = _dbContext.news_detail.ToList();
            foreach (var news in newsList)
            {
                newsDetailList.Add(new NewsDataViewModel {
                    News_Detail = news,
                    Author = authors.Where(a => a.id_authors == news.id_authors).FirstOrDefault(),
                    Source = webNames.Where(w => w.name_id == news.id_web).FirstOrDefault(),
                    Category = _dbContext.categories.Where(c => c.id_categories == news.id_categories).FirstOrDefault()
            });
        }
            return View(newsDetailList);
        }
        public ActionResult CalculateNewByScore(int? id)
        {
            try
            {
                var silarities = _dbContext.similarities.Where(s => s.scrapednewsID == id && s.score.ToString().Contains("0.1")).Select(n => n.othersnewsID).ToList();
                var newsScr = _dbContext.news_detail.Where(n => silarities.Contains(n.news_id)).ToList();
                var authors = _dbContext.authors.ToList();
                var webNames = _dbContext.web_name.ToList();
                List<NewsDataViewModel> newsDetailList = new List<NewsDataViewModel>();

                
                foreach (var news in newsScr)
                {
                    newsDetailList.Add(new NewsDataViewModel
                    {
                        News_Detail = news,
                        Author = authors.Where(a => a.id_authors == news.id_authors).FirstOrDefault(),
                        Source = webNames.Where(w => w.name_id == news.id_web).FirstOrDefault(),
                        Category = _dbContext.categories.Where(c => c.id_categories == news.id_categories).FirstOrDefault()

                    });
                }
              
                return PartialView("~/Views/Home/_RenderNews.cshtml", newsDetailList);
            }
            catch (Exception)
            {
                throw;
            }
        }
        public ActionResult GetNationalNews()
        {
            try
            {
                var authors = _dbContext.authors.ToList();
                var webNames = _dbContext.web_name.ToList();
                List<NewsDataViewModel> newsDetailList = new List<NewsDataViewModel>();
                var newsList = _dbContext.news_detail.Where(n => n.id_categories == 2).ToList();
                foreach (var news in newsList)
                {
                    newsDetailList.Add(new NewsDataViewModel
                    {
                        News_Detail = news,
                        Author = authors.Where(a => a.id_authors == news.id_authors).FirstOrDefault(),
                        Source = webNames.Where(w => w.name_id == news.id_web).FirstOrDefault(),
                        Category = _dbContext.categories.Where(c => c.id_categories == news.id_categories).FirstOrDefault()

                    });
                }

                    return PartialView("~/Views/Home/_RenderNews.cshtml", newsDetailList);
            }
            catch (Exception ex)
            {
                return Content(ex.Message);
            }
        }
        public ActionResult GetSportNews()
        {
            try
            {
                var authors = _dbContext.authors.ToList();
                var webNames = _dbContext.web_name.ToList();
                List<NewsDataViewModel> newsDetailList = new List<NewsDataViewModel>();
                var newsList = _dbContext.news_detail.Where(n => n.id_categories == 1).ToList();
                foreach (var news in newsList)
                {
                    newsDetailList.Add(new NewsDataViewModel
                    {
                        News_Detail = news,
                        Author = authors.Where(a => a.id_authors == news.id_authors).FirstOrDefault(),
                        Source = webNames.Where(w => w.name_id == news.id_web).FirstOrDefault(),
                        Category = _dbContext.categories.Where(c => c.id_categories == news.id_categories).FirstOrDefault()

                    });
                }
                return PartialView("~/Views/Home/_RenderNews.cshtml", newsDetailList);
            }
            catch (Exception ex)
            {
                return Content(ex.Message);
            }
        }
        public ActionResult GetFilterByDateAndCheck(FilterDateOrCheck filterObject)
        {
            try
            {
                var authors = _dbContext.authors.ToList();
                var webNames = _dbContext.web_name.ToList();
                List<NewsDataViewModel> newsDetailList = new List<NewsDataViewModel>();
                List<news_detail> newsList = new List<news_detail>();
                if (filterObject.DawnNews == true && filterObject.PakistanToday == true)
                    newsList = _dbContext.news_detail.ToList();

                else if(filterObject.DawnNews == true && filterObject.PakistanToday == false)
                    newsList = _dbContext.news_detail.Where(n => n.id_web == 1).ToList();

                else if(filterObject.DawnNews == false && filterObject.PakistanToday == true)
                    newsList = _dbContext.news_detail.Where(n => n.id_web == 2).ToList();

                else if (filterObject.DawnNews == false && filterObject.PakistanToday == false)
                    newsList = _dbContext.news_detail.ToList();
                var listToCastDate = new List<NewsCastDate>();
                if (filterObject.ToDate != null && filterObject.FromDate != null)
                {
                    newsList = newsList.Where(n => Convert.ToDateTime(n.date) >= Convert.ToDateTime(filterObject.ToDate) &&
                    Convert.ToDateTime(n.date) <= Convert.ToDateTime(filterObject.FromDate)).ToList();

                }



                foreach (var news in newsList)
                {
                   
                    newsDetailList.Add(new NewsDataViewModel
                    {
                        News_Detail = news,
                        Author = authors.Where(a => a.id_authors == news.id_authors).FirstOrDefault(),
                        Source = webNames.Where(w => w.name_id == news.id_web).FirstOrDefault(),
                        Category = _dbContext.categories.Where(c => c.id_categories == news.id_categories).FirstOrDefault()

                    });
                }
                return PartialView("~/Views/Home/_RenderNews.cshtml", newsDetailList);
            }
            catch (Exception ex)
            {
                return Content(ex.Message);
            }
        }
        public ActionResult ShowNewsDetail(int id)
        {
            try
            {
                NewsDataViewModel newsDetailList = new NewsDataViewModel();
                var newsList = _dbContext.news_detail.FirstOrDefault(n => n.news_id == id);

                newsDetailList.News_Detail = newsList;
                newsDetailList.Author = _dbContext.authors.FirstOrDefault(n => n.id_authors == newsList.id_authors);
                newsDetailList.Source = _dbContext.web_name.FirstOrDefault(n => n.name_id == newsList.id_web);
                newsDetailList.Source = _dbContext.web_name.FirstOrDefault(n => n.name_id == newsList.id_web);

                return View(newsDetailList);
            }
            catch (Exception ex)
            {
                return Content(ex.Message);
            }
        }
        public ActionResult SearchByHeading(SearchViewModel filterObject)
        {
            try
            {

                var authors = _dbContext.authors.ToList();
                var webNames = _dbContext.web_name.ToList();
                List<NewsDataViewModel> newsDetailList = new List<NewsDataViewModel>();
                var newsList = _dbContext.news_detail.Where(n => n.heading.Contains(filterObject.Heading)).ToList();
                foreach (var news in newsList)
                {
                    newsDetailList.Add(new NewsDataViewModel
                    {
                        News_Detail = news,
                        Author = authors.Where(a => a.id_authors == news.id_authors).FirstOrDefault(),
                        Source = webNames.Where(w => w.name_id == news.id_web).FirstOrDefault(),
                        Category = _dbContext.categories.Where(c => c.id_categories == news.id_categories).FirstOrDefault()

                    });
                }
                return PartialView("~/Views/Home/_RenderNews.cshtml", newsDetailList);
            }
            catch (Exception ex)
            {
                return Content(ex.Message);
            }
        }
        
        public ActionResult About()
        {
            ViewBag.Message = "Your application description page.";

            return View();
        }

        public ActionResult Contact()
        {
            ViewBag.Message = "Your contact page.";

            return View();
        }
    }
}