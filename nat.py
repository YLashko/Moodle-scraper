from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fpdf import FPDF
from os import remove
pdf = FPDF()
pdf.add_font('true_arial', '', 'arial-unicode-ms.ttf', uni = True)
pdf.set_font('true_arial', '', 12)
pdf.add_page()

PATH = 'C:\Program Files (x86)\Chromedriverp\chromedriver.exe'
ENTER = Keys.RETURN

blacklist = [
    '',
    'Регистрационное свидетельство СДО Moodle',
    'Наш адрес: г.Минск, ул.Советская,18, корп.2, каб.03а',
    'Задать вопрос службе техподдержки:',
    '   от преподавателя',
    '   от студента',
    'С чего начать?',
    'Информация для преподавателей, начинающих работу в СДО Moodle',
    'Наши услуги',
    'Полезные ссылки',
    'Со времени Вашего последнего входа ничего не произошло'
]
lection_end = [
    'конец лекции'
]

class Moodle_stealer:
    def __init__(self) -> None:
        self.webdriver = webdriver.Chrome(PATH)
        self.clear_pdf()
    
    def clear_pdf(self):
        self.txt = ''
        self.text_arr = []
    
    def open_moodle(self):
        self.webdriver.get('https://bspu.by/moodle/course/view.php?id=1747')
    
    def login(self, password):
        self.webdriver.find_element_by_xpath('//*[@id="username"]').send_keys(password) 
        self.webdriver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
        self.webdriver.find_element_by_xpath('//*[@id="loginbtn"]').click()       
    
    def copy_lection_text(self):
        stealed = self.webdriver.find_elements_by_tag_name('p')
        text = []
        for t in stealed:
            if (not t.text in blacklist) and ((not t.text in self.text_arr) or len(t.text) <= 7):
                text.append(t.text)
                self.text_arr.append(t.text)
                pdf.write(txt = t.text)
                pdf.ln(5)
        self.txt += '\n'.join(text)
        print(text)
    
    def click_next(self):
        try:
            if not self.webdriver.find_element_by_css_selector("[class='btn btn-secondary']").text.lower() in lection_end:
                self.webdriver.find_element_by_css_selector("[class='btn btn-secondary']").click()
            else:
                return False
            return True
        except:
            return False
    
    def save_lection(self):
        name = input()
        if name == 'Стоп':
            return 'Stop'
        self.write_topic(name)
        while True:
            self.copy_lection_text()
            if not self.click_next():
                break
        return ''

    def write_topic(self, topic):
        pdf.ln(10)
        pdf.set_font('true_arial', '', 16)
        pdf.write(txt = topic)
        pdf.set_font('true_arial', '', 12)
        pdf.ln(5)

    def write_to_txt(self, name):
        try:
            remove(name + '.pdf')
        except:
            pass  
        pdf.output(name + '.pdf')
        with open(f'{name}.txt', 'w') as file:
            file.write(self.txt)
        

mdl = Moodle_stealer()
mdl.open_moodle()
mdl.login('Password was removed')
while True:
    if mdl.save_lection() == 'Stop':
        mdl.write_to_txt(input('Имя файла: '))
        break