#! /usr/bin/env python3

import os
from bs4 import BeautifulSoup
import urllib.request


all_collections = ['p120701coll15', 'LSU_ACT', 'p15140coll30', 'AWW', 'AAW', 'ABW', 'p16313coll1', 
              'p15140coll12', 'APC', 'p120701coll17', 'ACC', 'LSUBK01', 'p16313coll34', 'BBA',
              'BRS', 'BTW', 'CMPRT', 'CWD', 'p16313coll89', 'LSA', 'CLF', 'LSU_CLT', 'p16313coll23',
              'LSU_CNP', 'p15140coll10', 'LSU_CWP', 'p16313coll21', 'p16313coll56', 'CRD', 'LSU_DYP',
              'p16313coll76', 'LSU_CFF', 'p16313coll9', 'p15140coll26', 'p16313coll26', 'p16313coll86',
              'p15140coll46', 'FJC', 'FBM', 'p16313coll51', 'LSU_GSC', 'p16313coll20', 'LSU_GCS',
              'GFM', 'LSU_GFM', 'p120701coll26', 'p16313coll8', 'p16313coll92', 'p120701coll10',
              'p16313coll17', 'HWJ', 'p15140coll18', 'HIC', 'LSU_BRT', 'PSL', 'p120701coll27',
              'HPL', 'LSU_HPL', 'IBE', 'p120701coll29', 'JSN', 'p16313coll24', 'LSU_JJA', 'LSU_WLS',
              'p16313coll81', 'JNT', 'p15140coll1', 'p120701coll28', 'UNO_JBF', 'p15140coll31',
              'p16313coll25', 'p120701coll9', 'LOU', 'p15140coll6', 'p16313coll19', 'LSU_LHC',
              'p16313coll48', 'RJR', 'p16313coll65', 'p16313coll45', 'p15140coll41', 'LSU_PVC',
              'p16313coll62', 'p120701coll13', 'p16313coll52', 'LSU_LNP', 'p16313coll22', 'LPC',
              'lapur', 'p16313coll79', 'p16313coll80', 'LST', 'p15140coll21', 'p15140coll35',
              'LSAP', 'p16313coll77', 'p267101coll4', 'HLM', 'LSM_CCC', 'LCT', 'LSM_NCC', 'LHC',
              'LSM_KOH', 'JAZ', 'LSM_NAC', 'LSM_MPC', 'p120701coll18', 'LSM_FQA', 'p16313coll31',
              'LWP', 'LMNP01', 'p16313coll87', 'LOYOLA_ETD', 'p16313coll44', 'p16313coll98',
              'p16313coll91', 'p16313coll5', 'p16313coll28', 'TLD', 'p15140coll49', 'LSUHSC_NCC',
              'p16313coll3', 'p15140coll44', 'p15140coll23', 'LSUHSCS_GWM', 'p120701coll12',
              'p15140coll17', 'p16313coll10', 'LSU_RBC', 'p16313coll35', 'p16313coll69',
              'p120701coll7', 'LSU_SCE', 'LSU_UAP', 'p120701coll24', 'p16313coll85', 'p15140coll28',
              'LMP', 'p15140coll42', 'LSU_MDP', 'MPF', 'p16313coll43', 'p16313coll74', 'MMF', 'MPA',
              'p16313coll54', 'LSU_MRF', 'LSU_NMI', 'LOH', 'NCC', 'MSW', 'LSU_NOE', 'CCA', 'NewOrleans',
              'NONegExposures', 'p16313coll95', 'p16313coll93', 'p15140coll27', 'NWM', 'OMSA', 'OSC',
              'p15140coll4', 'p16313coll72', 'LPH', 'LPS', 'SartainEngravings', 'RTP', 'p15140coll60',
              'p16313coll83', 'p16313coll61', 'RMC', 'RTC', 'RSP', 'p120701coll19', 'p15140coll56',
              'SIP', 'LHP', 'p16313coll2', 'STC', 'THW', 'LSU_FCC', 'LSU_RBO', 'p120701coll22',
              'p15140coll14', 'p120701coll23', 'p120701coll8', 'Tensas', 'p15140coll52', 'LSU_TJP',
              'p15140coll16', 'LSUS_TBP', 'p120701coll25', 'UNO_ANI', 'p15140coll7', 'p15140coll50',
              'VBC', 'p15140coll51', 'p16313coll58', 'p15140coll19', 'p15140coll54', 'p16313coll57',
              'wri-boy', 'p16313coll96'
              ]

for alias in all_collections:
    print(alias)
    os.makedirs('Abouts_scraped/{}'.format(alias), exist_ok=True)
    if os.path.isfile('Abouts_scraped/{}/{}.html'.format(alias, alias)):
        with open('Abouts_scraped/{}/{}.html'.format(alias, alias), 'r') as f:
            soup = BeautifulSoup(f, 'lxml')
    else:
        url = 'http://cdm16313.contentdm.oclc.org/cdm/about/collection/{}'.format(alias)
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page, 'lxml')
        if "The LOUISiana Digital Library (LDL) is an online library of Louisiana institutions that provides over 144,000 digital materials." in soup.prettify():
            continue
        with open('Abouts_scraped/{}/{}.html'.format(alias, alias), 'w') as f:
            f.write(soup.prettify())

    if not os.path.isfile('Abouts_scraped/{}/{}_condensedtext.txt'.format(alias, alias)):
        about_this = [i for i in soup.find_all("div") if "id" in i.attrs and 'top_content' in i["id"]]
        header_text = [i.get_text() for i in about_this[0].find_all("p")]
        about_header = " ".join(i.strip() for i in header_text if i)
        paragraph_texts = [i.get_text().replace('\n', ' ').strip() for i in about_this[0].find_all("p") if i]
        paragraph = ' '.join(i.strip() for i in paragraph_texts)
        paragraph = ' '.join(paragraph.split())
        print(paragraph)
        with open('Abouts_scraped/{}/{}_condensedtext.txt'.format(alias, alias), 'w') as f:
            f.write(paragraph)

    if not os.path.isfile('Abouts_scraped/{}/{}_strippedtext.txt'.format(alias, alias)):
        about_this = [i for i in soup.find_all("div") if "id" in i.attrs and 'top_content' in i["id"]]
        header_text = [i.string for i in about_this[0].find_all("p")]
        if header_text:
            about_header = " ".join(i.strip() for i in header_text if i)
            paragraph_texts = " ".join(str(i).strip() for i in about_this[0].find_all("p"))
            print(paragraph_texts.strip())
            with open('Abouts_scraped/{}/{}_strippedtext.txt'.format(alias, alias), 'w') as f:
                f.write(paragraph_texts.strip())

    for imglink in (i for i in soup.find_all('img')):
        os.makedirs('Abouts_scraped/{}/images/staticcontent'.format(alias), exist_ok=True)
        if 'getstaticcontent' in imglink['src']:
            continue
            namelist = imglink['src'].split('/')
            name = namelist[-3]
            filename = 'Abouts_scraped/{}/images/staticcontent/{}'.format(alias, name)
            imgurl = 'https://cdm16313.contentdm.oclc.org/{}'.format(imglink['src'])
        elif 'getthumbnail' in imglink['src']:
            continue
            os.makedirs('Abouts_scraped/{}/images/sidebarthumbs/'.format(alias), exist_ok=True)
            namelist = imglink['src'].split('/')
            name = namelist[-1]
            filename = 'Abouts_scraped/{}/images/sidebarthumbs/{}'.format(alias, name)
            imgurl = 'https://cdm16313.contentdm.oclc.org/{}'.format(imglink['src'])
        else:
            os.makedirs('Abouts_scraped/{}/images/good/'.format(alias), exist_ok=True)
            namelist = imglink['src'].split('/')
            name = namelist[-1]
            if '.png' in name or '.jpg' in name or '.gif' in name:
                filetype = ''
            else:
                filetype = '.jpg'
            name = "".join(i for i in name if i.isalnum() or i == ".")
            filename = 'Abouts_scraped/{}/images/good/{}{}'.format(alias, name, filetype)
            if '.org' in imglink['src'] or '.com' in imglink['src'] or '.edu' in imglink['src']:
                imgurl = imglink['src']
            else:
                imgurl = 'https://cdm16313.contentdm.oclc.org{}'.format(imglink['src'])
        imgurl = imgurl.replace(' ', '%20')
        filename = filename.replace(' ', '')
        if not os.path.isfile(filename):
            print(filename)
            try:
                with urllib.request.urlopen(imgurl) as response:
                    binary = response.read()
                with open(filename, 'bw') as f:
                    f.write(binary)
            except Exception as e:
                print(e)
