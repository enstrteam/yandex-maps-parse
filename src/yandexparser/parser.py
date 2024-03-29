import os
import pandas as pd

class InfoParser:

    day_of_week = {
        'Mo': 'Monday',
        'Tu': 'Tuesday',
        'We': 'Wednesday',
        'Th': 'Thursday',
        'Fr': 'Friday',
        'Sa': 'Saturday',
        'Su': 'Sunday'
    }

    def __init__(self, data) -> None:
        self.data = data

    def parse(self, format=None):

        json_data = {
            'category': self.data['category'],
            'name': self.data['name'],
            'phone': self.data['phone'].replace(' ', '').replace('-','').replace('(','').replace(')','') if self.data['phone'] else 'no phone',
            'address': self.data['address'],
            'rating': float(self.data['rating'].replace(',','.')) if self.data['rating'] else 0,
            'website': "https://" + self.data['website'] if self.data['website'] else "",
            'social_links': self.data['social_links'],
            'opening_hours': {self.day_of_week[i.split(" ")[0]]:i.split(' ')[1] for i in self.data['opening_hours']}
            }
        
        if format == 'json':            
            return json_data
        
        csv_data = json_data
        csv_data.popitem()
        csv_data.popitem()


        return csv_data
    
    def output(self, city, category, area):
        
        dir = '../output'
        if not os.path.exists(dir):
            os.makedirs(dir)

        output_path = f'{dir}/{city}-{area + " -" if area else ""}{category}.csv'

        df = pd.DataFrame(self.parse(), index=[1])
        df.to_csv(output_path, index=False, mode='a', header=False)
            
