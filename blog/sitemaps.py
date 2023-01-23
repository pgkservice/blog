from django.contrib.sitemaps import SiteMap
from .models import Post




class PostSiteMap(SiteMap):
	changefreq = "weekly"
	priority = 0.9


	def items(self):
		return Post.published.all()


	def lastmod(self, obj):
		return obj.updated 
	