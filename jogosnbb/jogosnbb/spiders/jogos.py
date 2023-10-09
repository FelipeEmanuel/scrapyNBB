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
        padrao2 = r'(\d+)[+](\d+)'
        
        request = {
            'campeonatoAno': response.request.meta['campeonatoAno'],
            'fase': response.request.meta['fase'],
            'timeCasa': response.request.meta['timeCasa'],
            'pontosTimeCasa': int(response.request.meta['pontosTimeCasa']),
            
            'acertos2PtsTimeCasa' : int(re.search(padrao, response.css('table.team_general_table tfooter td:nth-child(8)::text').get()).group(1)),
            'acertos3PtsTimeCasa' : int(re.search(padrao, response.css('table.team_general_table tfooter td:nth-child(7)::text').get()).group(1)),         
            'acertosTotaisTimeCasa' :  int(re.search(padrao, response.css('table.team_general_table tfooter td:nth-child(8)::text').get()).group(1)) + 
                                        int(re.search(padrao, response.css('table.team_general_table tfooter td:nth-child(7)::text').get()).group(1)),                                   
            'LancesLivresCertosTimeCasa' : int(re.search(padrao, response.css('table.team_general_table tfooter td:nth-child(9)::text').get()).group(1)), 
            'rebotesDefensivosTimeCasa' : int(re.search(padrao2, response.css('table.team_general_table tfooter td:nth-child(5)::text').get()).group(1)),
            'rebotesOfensivosTimeCasa' : int(re.search(padrao2, response.css('table.team_general_table tfooter td:nth-child(5)::text').get()).group(2)),
            'rebotesTotaisTimeCasa' :  int(re.search(padrao2, response.css('table.team_general_table tfooter td:nth-child(5)::text').get()).group(1)) +
                                        int(re.search(padrao2, response.css('table.team_general_table tfooter td:nth-child(5)::text').get()).group(2)),         
            'assistsTimeCasa' : int(response.css('table.team_general_table tfooter td:nth-child(6)::text').get()),           
            'RoubadasTimeCasa' : int(response.css('table.team_general_table tfooter td:nth-child(10)::text').get()),
            'ErrosTimeCasa' : int(response.css('table.team_general_table tfooter td:nth-child(14)::text').get()),  
            'TocosTimeCasa' : int(response.css('table.team_general_table tfooter td:nth-child(11)::text').get()),
            'FaltasTimeCasa' : int(float(response.css('table.team_general_table tfooter td:nth-child(12)::text').get())),
            'EficienciaTimeCasa' : int(response.css('table.team_general_table tfooter td:nth-child(17)::text').get()),
            
            'Arremessos2PtsTimeCasa' : int(re.search(padrao, response.css('table.team_general_table tfooter td:nth-child(8)::text').get()).group(2)),
            'Arremessos3PtsTimeCasa' : int(re.search(padrao, response.css('table.team_general_table tfooter td:nth-child(7)::text').get()).group(2)),
            'ArremessosLLTimeCasa' : int(re.search(padrao, response.css('table.team_general_table tfooter td:nth-child(9)::text').get()).group(2)),
            'ArremessosTotaisTimeCasa' : int(re.search(padrao, response.css('table.team_general_table tfooter td:nth-child(8)::text').get()).group(2)) + 
                                        int(re.search(padrao, response.css('table.team_general_table tfooter td:nth-child(7)::text').get()).group(2)),
            
            'timeFora': response.request.meta['timeFora'],
            'pontosTimeFora': int(response.request.meta['pontosTimeFora']),
            'acertos2PtsTimeFora' : int(re.search(padrao, response.css('table.team_two_table tfooter td:nth-child(8)::text').get()).group(1)),
            'acertos3PtsTimeFora' : int(re.search(padrao, response.css('table.team_two_table tfooter td:nth-child(7)::text').get()).group(1)),
            'acertosTotaisTimeFora' :  int(re.search(padrao, response.css('table.team_two_table tfooter td:nth-child(8)::text').get()).group(1)) +
                                        int(re.search(padrao, response.css('table.team_two_table tfooter td:nth-child(7)::text').get()).group(1)),
            'LancesLivresCertosTimeFora' : int(re.search(padrao, response.css('table.team_two_table tfooter td:nth-child(9)::text').get()).group(1)),
            'rebotesDefensivosTimeFora' : int(re.search(padrao2, response.css('table.team_two_table tfooter td:nth-child(5)::text').get()).group(1)),
            'rebotesOfensivosTimeFora' : int(re.search(padrao2, response.css('table.team_two_table tfooter td:nth-child(5)::text').get()).group(2)),
            'rebotesTotaisTimeFora' :  int(re.search(padrao2, response.css('table.team_two_table tfooter td:nth-child(5)::text').get()).group(1)) + 
                                        int(re.search(padrao2, response.css('table.team_two_table tfooter td:nth-child(5)::text').get()).group(2)),
            'assistsTimeFora' : int(response.css('table.team_two_table tfooter td:nth-child(6)::text').get()),
            'RoubadasTimeFora' : int(response.css('table.team_two_table tfooter td:nth-child(10)::text').get()),
            'ErrosTimeFora' : int(response.css('table.team_two_table tfooter td:nth-child(14)::text').get()),
            'TocosTimeFora' : int(response.css('table.team_two_table tfooter td:nth-child(11)::text').get()),
            'FaltasTimeFora' : int(float(response.css('table.team_two_table tfooter td:nth-child(12)::text').get())),
            'EficienciaTimeFora' : int(response.css('table.team_two_table tfooter td:nth-child(17)::text').get()),
            
            'Arremessos2PtsTimeFora' : int(re.search(padrao, response.css('table.team_two_table tfooter td:nth-child(8)::text').get()).group(2)),
            'Arremessos3PtsTimeFora' : int(re.search(padrao, response.css('table.team_two_table tfooter td:nth-child(7)::text').get()).group(2)),
            'ArremessosLLTimeFora' : int(re.search(padrao, response.css('table.team_two_table tfooter td:nth-child(9)::text').get()).group(2)),
            'ArremessosTotaisTimeFora' : int(re.search(padrao, response.css('table.team_two_table tfooter td:nth-child(8)::text').get()).group(2)) +
                                            int(re.search(padrao, response.css('table.team_two_table tfooter td:nth-child(7)::text').get()).group(2)),
            
        }
        
        yield request
        
