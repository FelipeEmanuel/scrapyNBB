import scrapy
import re

class JogosSpider(scrapy.Spider):
    name = 'jogos'
    start_urls = ['https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=71']
    
    def parse(self, response): 
        next = ['63', '59']
        i = 0
        jogos = response.css('tbody tr')
        for jogo in jogos:
            
            gameInfo = jogo.css('td.score_value a ::attr(href)').get()
            fase = jogo.css('td.stage_value::text').get()
            timeCasa = jogo.css('td.home_team_value span::text').get()
            pontosTimeCasa = jogo.css('td.score_value a span.home::text').get()
            pontosTimeFora = jogo.css('td.score_value a span.away::text').get()
            timeFora = jogo.css('td.visitor_team_value span::text').get()
            campeonatoAno = jogo.css('td.champ_value::text').get()
            
            
            resp_meta = {
                'fase': fase,
                'timeCasa': timeCasa,
                'pontosTimeCasa': pontosTimeCasa,
                'pontosTimeFora': pontosTimeFora,
                'timeFora': timeFora,
                'campeonatoAno': campeonatoAno,
            }   
            yield response.follow(gameInfo, callback=self.parse_game_info, meta=resp_meta)
            
        while i < len(next):
            next_url = 'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=' + next[i]
            i+=1
            yield response.follow(next_url, callback=self.parse)
          
            
             
    def parse_game_info(self, response):
        padrao = r'(\d+)/(\d+)'
          
        request = {
            'campeonatoAno': response.request.meta['campeonatoAno'],
            'fase': response.request.meta['fase'],
            'timeCasa': response.request.meta['timeCasa'],
            'pontosTimeCasa': int(response.request.meta['pontosTimeCasa']),
            'acertos3PtsTimeCasa' : int(response.css('div.A3C .widget_value_one span::text').get()),           
            'acertos2PtsTimeCasa' : int(response.css('div.A2C .widget_value_one span::text').get()),
            'acertosTotaisTimeCasa' :  int(response.css('div.A3C .widget_value_one span::text').get()) + int(response.css('div.A2C .widget_value_one span::text').get()),          
            'LanceLivreTimeCasa' : int(response.css('div.LLC .widget_value_one span::text').get()), 
            'rebotesTimeCasa' : int(response.css('div.RT .widget_value_one span::text').get()),           
            'assistsTimeCasa' : int(response.css('div.ASS .widget_value_one span::text').get()),           
            'RoubadasTimeCasa' : int(response.css('div.BR .widget_value_one span::text').get()),  
            'TocosTimeCasa' : int(response.css('div.TO .widget_value_one span::text').get()),
            'FaltasTimeCasa' : int(response.css('div.FC .widget_value_one span::text').get()),
            'EficienciaTimeCasa' : int(response.css('div.EF .widget_value_one span::text').get()),
            'Arremessos2PtsTimeCasa' : int(re.search(padrao, response.css('table.team_general_table tfooter td:nth-child(8)::text').get()).group(2)),
            'Arremessos3PtsTimeCasa' : int(re.search(padrao, response.css('table.team_general_table tfooter td:nth-child(7)::text').get()).group(2)),
            'ArremessosLLTimeCasa' : int(re.search(padrao, response.css('table.team_general_table tfooter td:nth-child(9)::text').get()).group(2)),
            'ArremessosTotaisTimeCasa' : int(re.search(padrao, response.css('table.team_general_table tfooter td:nth-child(8)::text').get()).group(2)) + int(re.search(padrao, response.css('table.team_general_table tfooter td:nth-child(7)::text').get()).group(2)),
            'timeFora': response.request.meta['timeFora'],
            'pontosTimeFora': int(response.request.meta['pontosTimeFora']),
            'acertos3PtsTimeFora' : int(response.css('div.A3C .widget_value_two span::text').get()),
            'acertos2PtsTimeFora' : int(response.css('div.A2C .widget_value_two span::text').get()),
            'acertosTotaisTimeFora' :  int(response.css('div.A3C .widget_value_two span::text').get()) + int(response.css('div.A2C .widget_value_two span::text').get()),
            'LanceLivreTimeFora' : int(response.css('div.LLC .widget_value_two span::text').get()),
            'rebotesTimeFora' : int(response.css('div.RT .widget_value_two span::text').get()),
            'assistsTimeFora' : int(response.css('div.ASS .widget_value_two span::text').get()),
            'RoubadasTimeFora' : int(response.css('div.BR .widget_value_two span::text').get()),
            'TocosTimeFora' : int(response.css('div.TO .widget_value_two span::text').get()),
            'FaltasTimeFora' : int(response.css('div.FC .widget_value_two span::text').get()),
            'EficienciaTimeFora' : int(response.css('div.EF .widget_value_two span::text').get()),
            'Arremessos2PtsTimeFora' : int(re.search(padrao, response.css('table.team_two_table tfooter td:nth-child(8)::text').get()).group(2)),
            'Arremessos3PtsTimeFora' : int(re.search(padrao, response.css('table.team_two_table tfooter td:nth-child(7)::text').get()).group(2)),
            'ArremessosLLTimeFora' : int(re.search(padrao, response.css('table.team_two_table tfooter td:nth-child(9)::text').get()).group(2)),
            'ArremessosTotaisTimeFora' : int(re.search(padrao, response.css('table.team_two_table tfooter td:nth-child(8)::text').get()).group(2)) + int(re.search(padrao, response.css('table.team_two_table tfooter td:nth-child(7)::text').get()).group(2))
        }
        
        yield request
        
