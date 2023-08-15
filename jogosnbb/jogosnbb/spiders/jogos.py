import scrapy

class JogosSpider(scrapy.Spider):
    name = 'jogos'
    start_urls = ['https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=71']
    
    def parse(self, response): 
        next = ['63', '59', '54', '47', '41', '34', '27', '20', '15', '8', '4', '3', '2', '1']
        i = 0
        jogos = response.css('tbody tr')
        for jogo in jogos:
            
            gameInfo = jogo.css('td.score_value a ::attr(href)').get()
            fase = jogo.css('td.stage_value::text').get()
            data = jogo.css('td.date_value span::text').get()
            timeCasa = jogo.css('td.home_team_value span::text').get()
            pontosTimeCasa = jogo.css('td.score_value a span.home::text').get()
            pontosTimeFora = jogo.css('td.score_value a span.away::text').get()
            timeFora = jogo.css('td.visitor_team_value span::text').get()
            campeonatoAno = jogo.css('td.champ_value::text').get()
            ginasio = jogo.css('td.gym_value::text').get()
            
            resp_meta = {
                'fase': fase,
                'data': data,
                'timeCasa': timeCasa,
                'pontosTimeCasa': pontosTimeCasa,
                'pontosTimeFora': pontosTimeFora,
                'timeFora': timeFora,
                'campeonatoAno': campeonatoAno,
                'ginasio': ginasio
            }   
            yield response.follow(gameInfo, callback=self.parse_game_info, meta=resp_meta)
            
        while i < len(next):
            next_url = 'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=' + next[i]
            i+=1
            yield response.follow(next_url, callback=self.parse)
            
            
             
    def parse_game_info(self, response):
            
        request = {
            'data': response.request.meta['data'],
            'campeonatoAno': response.request.meta['campeonatoAno'],
            'ginasio': response.request.meta['ginasio'],
            'fase': response.request.meta['fase'],
            'timeCasa': response.request.meta['timeCasa'],
            'pontosTimeCasa': response.request.meta['pontosTimeCasa'],
            'acertos3PtsTimeCasa' : response.css('div.A3C .widget_value_one span::text').get(),           
            'acertos2PtsTimeCasa' : response.css('div.A2C .widget_value_one span::text').get(),           
            'LanceLivreTimeCasa' : response.css('div.LLC .widget_value_one span::text').get(), 
            'rebotesTimeCasa' : response.css('div.RT .widget_value_one span::text').get(),           
            'assistsTimeCasa' : response.css('div.ASS .widget_value_one span::text').get(),           
            'RoubadasTimeCasa' : response.css('div.BR .widget_value_one span::text').get(),  
            'TocosTimeCasa' : response.css('div.TO .widget_value_one span::text').get(),
            'FaltasTimeCasa' : response.css('div.FC .widget_value_one span::text').get(),
            'timeFora': response.request.meta['timeFora'],
            'pontosTimeFora': response.request.meta['pontosTimeFora'],
            'acertos3PtsTimeFora' : response.css('div.A3C .widget_value_two span::text').get(),
            'acertos2PtsTimeFora' : response.css('div.A2C .widget_value_two span::text').get(),
            'LanceLivreTimeFora' : response.css('div.LLC .widget_value_two span::text').get(),
            'rebotesTimeFora' : response.css('div.RT .widget_value_two span::text').get(),
            'assistsTimeFora' : response.css('div.ASS .widget_value_two span::text').get(),
            'RoubadasTimeFora' : response.css('div.BR .widget_value_two span::text').get(),
            'TocosTimeFora' : response.css('div.TO .widget_value_two span::text').get(),
            'FaltasTimeFora' : response.css('div.FC .widget_value_two span::text').get()
        }
        
        yield request
        
