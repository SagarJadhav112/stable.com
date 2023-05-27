import scrapy


class StabaleSpider(scrapy.Spider):
    name = 'stable'
    count = 0
    count_1 = 0
    max_count= 3
    max_count_1 =8
   
    def start_requests(self):
        url ="https://stablediffusionapi.com/models?page="
        cokkies = {"XSRF-TOKEN":"eyJpdiI6Ii9LR2VCNUViTHkzYWczRjB4cTBtR1E9PSIsInZhbHVlIjoiSVRQRTR4UUxKSDFIMXErNUxORlB0ZGtSS3dSdUpiSkJPMExUWkJMNUxEUStXY3JoeUE0Z2ExeEJjZTJwajVlQ3Bya1J5RTZDTmx6a2dxdUlOam1NcVIrUTVBUkEzc1RzZldhcmF5eFVZSFBOMG9wL1lYdjNOVHpMN0xZajBZMzEiLCJtYWMiOiIzMzNiY2NlNGExOTgyYzUzZWEwMTQxNjExNTllODNhYTJkYjA2OWRmNzJkZWY1ZTNlNzExZThiYzgxOWRjYzY2IiwidGFnIjoiIn0%3D",
                "sdapi_session":"eyJpdiI6InFCT2c1STVUblg1QzcyUkN2RXJjaEE9PSIsInZhbHVlIjoidGhqSEVyTHFwYTVzSVBMY0xTWEorOGtyTVg1TjhTQk0vSk1vTTRQbTlBUzRrMzhFQWhUU3Z5NG5ZbjNWbzl5WXhTM1k4c3cycUtJcm5KWTBweUUzL01NbkZ1d2VJaVYrd2YwdkdZWUpDcW9YaEtkSWVxS3p4MlFHMkJhQXdNSjEiLCJtYWMiOiJkOTIzYTYzODM2ODEwNTkzZjI2OWEzM2NmNjQzYmRkYmUzYjViY2EzMWQ5MTg4Njg0MmI2NGQ3YmY4OGI4OGIwIiwidGFnIjoiIn0%3D"}
        yield scrapy.Request(url=url,method="GET",cookies=cokkies,
                             meta={"count_1":self.count_1,"page_1_count":0},                            
                                # dont_filter=True,
                             callback=self.parse)

    def parse(self, response):
        
        with open("xyz.html","w",encoding="utf-8")as a:

            a.write(response.text)
        container = response.xpath("//div[@class='relative']")
        for  i in container:
            titel = i.xpath('.//descendant::a[1]/text()').get()          
            link = i.xpath('.//descendant::a[1]/@href').get()
            inner = i.xpath(".//div[@class='wrap-container']/a/@href").get()
            
            if inner:
                yield scrapy.Request(url=inner,
                                 meta={"titel":titel,"link":link,
                                       "all_data":{titel:[]},
                                       "count":self.count,
                                       "count_1":self.count_1,
                                       "page_count":0,"page_1_count":0,                                  
                                       },
                                #   dont_filter=True,
                                 callback=self.innerside
                                 )
                # yield{
                #     "dp1":inner
                # }
        next_page = response.xpath("//a[@class='relative inline-flex items-center px-2 py-2 -ml-px text-sm font-medium leading-5 text-gray-700 transition duration-150 ease-in-out bg-white border border-gray-300 rounded-r-md hover:text-gray-800 focus:z-10 focus:outline-none focus:border-blue-300 focus:shadow-outline-blue active:bg-gray-100 active:text-gray-500']/@href").get()
        if next_page:           
            if self.max_count_1 > response.meta["page_1_count"]:
                response.meta["page_1_count"] += 1                                    
                yield scrapy.Request(url= next_page,meta={
                    "count_1":response.meta["count_1"],
                    "page_1_count":response.meta["page_1_count"],
                },
                # dont_filter=True
                                 callback=self.parse)
                        
    def innerside (self,resposne):
        # with open("abc.html","w",encoding="utf-8")as a:

        #     a.write(resposne.text)
        titel = resposne.meta.get("titel")

        container2= resposne.xpath("//div[@class='relative block w-full bg-gray-900 group rounded-2xl']")
        # try :
        #     id = resposne.xpath("//h3[contains(text(),'model_id ')]/text()").get().replace("model_id : ","")
        # except:
        #     id = ""

    
        # try:
        #     style =resposne.xpath("//h3[contains(text(),'Instance Prompt')]/text()").get().replace("Instance Prompt :","")
        # except:
        #     style = " "
        # try :
        #     first_image_text =resposne.xpath("//img[@id='image-0']/following::p[1]/text()").get()
        # except:
        #     first_image_text = " "
        
            
        # yield{
        #             "id":id,
        #             "style":style,
        #             "first_image_text": first_image_text
        #         }  
        for ww in container2:
            
            pic_link = ww.xpath("./img/@src").get()
            texts = ww.xpath(".//div[@class='relative p-2']//descendant::div[@class='p-4']/p/text()").get()
            
            # try :
            #     model_id = resposne.xpath("//h3[contains(text(),'model_id ')]/text()").get().replace("model_id : ","")

            # except:
            #     model_id =" "
            # try:
            #     style = resposne.xpath("//h3[contains(text(),'Instance Prompt')]/text()").get().replace("Instance Prompt :","")
            #     # print(style)
            # except:
            #     style =" " 
                  
            # yield{
            #     "model_id":model_id,
            #     "style":style
            # }       
            resposne.meta.get("all_data").get(resposne.meta.get("titel")).append({"pick_link":pic_link,"texts":texts})
            try:
                resposne.meta.get("all_data").get(resposne.meta.get("titel")).append({"texts":texts})
            except:
                pass
        
        next_page_inner = resposne.xpath("//p[contains(text(),'Showing')]//following::section[@class='py-8 lg:py-16']/preceding::a[1]/@href").get()
        if next_page_inner:
            if self.max_count > resposne.meta["page_count"]:
                resposne.meta["page_count"] += 1                
                yield scrapy.Request(url=next_page_inner,
                                    meta={"titel":titel,"link":resposne.meta["link"],
                                        "all_data":resposne.meta["all_data"],
                                            "count":resposne.meta["count"],
                                            "page_count":resposne.meta["page_count"],
                                    }
                                            # ,dont_filter= True
                                    , callback=self.innerside)
            else:
                pass
                resposne.meta["titel"]
            #     # yield{
            #     # "all_data":resposne.meta.get("all_data")
            # }
        else:
            yield{
                "all_data":resposne.meta.get("all_data")
            }
           
        
            
        
        
    
        
            
            