#! /usr/bin/python3

import pytest
import mock
import scrape_cDM


''' Run pytest from project root with: `pytest` '''


@pytest.fixture
def make_simple_object_etree():
    from lxml import etree as ET
    simple_object_xmltext = """<?xml version="1.0" encoding="UTF-8"?><xml><title>Some Title</title><contac>somename@some.org</contac><creato>Some Creator</creato><contri></contri><subjec>Some subject; And Another</subjec><credit>Some credits</credit><descri>Some desctiption</descri><notes>Some notes</notes><publis>Some published</publis><date>1776-07-04</date><type>Image</type><format>An item; A format</format><identi>An Identi</identi><source>A source</source><langua>en</langua><relati>http://louisdl.louislibraries.org/cdm4/browse.php?CISOROOT=/p111111coll11</relati><sourca></sourca><covera>Some Covera</covera><coverb>1900-01-25</coverb><rights>Some rights</rights><access>2001.0001.11</access><catlog>ABC</catlog><catalo>1492-04-15</catalo><object>jcm800</object><plugin></plugin><image>100</image><imaga>4</imaga><color>Some Color</color><extent></extent><imagb>Some Imagb</imagb><file>11 KB</file><hardwa></hardwa><digiti></digiti><digita></digita><fullrs></fullrs><find>1.jp2</find><dmaccess></dmaccess><dmimage></dmimage><dmcreated>2017-01-01</dmcreated><dmmodified>2104-04-02</dmmodified><dmoclcno></dmoclcno><dmrecord>0</dmrecord><restrictionCode>1</restrictionCode><cdmfilesize>13</cdmfilesize><cdmfilesizeformatted>1.60 MB</cdmfilesizeformatted><cdmprintpdf>0</cdmprintpdf><cdmhasocr>0</cdmhasocr><cdmisnewspaper>0</cdmisnewspaper></xml>"""
    simple_object_etree = ET.fromstring(bytes(bytearray(simple_object_xmltext, encoding='utf-8')))
    return simple_object_etree


@pytest.fixture
def make_pdfpage_page_etree():
    from lxml import etree as ET
    pdfpage_index_filetext = """<?xml version="1.0" encoding="utf-8"?><cpd><type>Document-PDF</type><page><pagetitle>Page 1</pagetitle><pagefile>3605.pdfpage</pagefile><pageptr>3604</pageptr></page></cpd>"""
    pdfpage_etree = ET.fromstring(bytes(bytearray(pdfpage_index_filetext, encoding='utf-8')))
    return pdfpage_etree.find('.//page')


@pytest.fixture
def make_coll_total_recs_etree():
    from lxml import etree as ET
    coll_total_recs_filetext = """<?xml version="1.0" encoding="UTF-8"?><results><totalrecs><suggestedtopic></suggestedtopic><total>20</total></totalrecs></results>"""
    coll_total_recs_etree = ET.fromstring(bytes(bytearray(coll_total_recs_filetext, encoding='utf-8')))
    return coll_total_recs_etree


def test_is_it_a_404_xml():
    error_return_text = """<?xml version="1.0" encoding="UTF-8"?><error><code>-2</code><message>Requested item not found</message><restrictionCode>-1</restrictionCode></error>"""
    assert scrape_cDM.is_it_a_404_xml(error_return_text) is True


def test_is_it_a_404_json():
    error_return_text = """{"code":"-2","message":"Requested item not found","restrictionCode":"-1"}"""
    assert scrape_cDM.is_it_a_404_json(error_return_text) is True


def test_has_pdfpage_elems(make_pdfpage_page_etree):
    assert scrape_cDM.has_pdfpage_elems(make_pdfpage_page_etree) is True


@mock.patch('scrape_cDM.ET')
def test_parse_binary_original_filetype(mock_ET, make_simple_object_etree):
    mock_ET.parse.return_value = make_simple_object_etree
    assert scrape_cDM.parse_binary_original_filetype('imag_path', 'imag_file') == 'jp2'
    mock_ET.parse.assert_called_with('imag_path/imag_file.xml')


@mock.patch('scrape_cDM.ET')
def test_count_root_objects(mock_ET, make_coll_total_recs_etree):
    mock_ET.parse.return_value = make_coll_total_recs_etree
    scrapealias = scrape_cDM.ScrapeAlias('_')
    scrapealias.alias_dir = 'imag_alias_dir'
    assert scrapealias.count_root_objects() == 20
    mock_ET.parse.assert_called_with('imag_alias_dir/Collection_TotalRecs.xml')


@mock.patch('scrape_cDM.ScrapeAlias.count_root_objects')
def test_calculate_chunks(mock_count_root_objects):
    scrapealias = scrape_cDM.ScrapeAlias('_')
    scrapealias.count_root_objects.return_value = 900
    assert scrapealias.calculate_chunks(100) == 10
    mock_count_root_objects.assert_called_with()

# @mock.patch('scrape_cDM.ScrapeAlias')
# def test_do_root_level_objects(mock_scrapealias):
#     scrapealias = mock_scrapealias('_')
#     # scrapealias.count_root_objects = mock_scrapealias.count_root_objects
#     # scrapealias.write_chunks_of_elems_in_collection = mock_scrapealias.write_chunks_of_elems_in_collection
#     # scrapealias.find_root_pointers_filetypes = mock_scrapealias.find_root_pointers_filetypes
#     # scrapealias.process_root_level_objects = mock_scrapealias.process_root_level_objects
#     scrapealias.count_root_objects.return_value = 1
#     assert scrapealias.num_chunks == 1
#     scrapealias.write_chunks_of_elems_in_collection = mock_scrapealias.write_chunks_of_elems_in_collection
#     scrapealias.find_root_pointers_filetypes = mock_scrapealias.find_root_pointers_filetypes
#     scrapealias.process_root_level_objects = mock_scrapealias.process_root_level_objects
