#! /usr/bin/python3

import pytest
from mock import patch
import scrape_cDM


''' Run pytest from project root with: `pytest` '''


@pytest.fixture
def simple_object_etree_fixture():
    from lxml import etree as ET
    simple_object_xmltext = """<?xml version="1.0" encoding="UTF-8"?><xml><title>Some Title</title><contac>somename@some.org</contac><creato>Some Creator</creato><contri></contri><subjec>Some subject; And Another</subjec><credit>Some credits</credit><descri>Some desctiption</descri><notes>Some notes</notes><publis>Some published</publis><date>1776-07-04</date><type>Image</type><format>An item; A format</format><identi>An Identi</identi><source>A source</source><langua>en</langua><relati>http://louisdl.louislibraries.org/cdm4/browse.php?CISOROOT=/p111111coll11</relati><sourca></sourca><covera>Some Covera</covera><coverb>1900-01-25</coverb><rights>Some rights</rights><access>2001.0001.11</access><catlog>ABC</catlog><catalo>1492-04-15</catalo><object>jcm800</object><plugin></plugin><image>100</image><imaga>4</imaga><color>Some Color</color><extent></extent><imagb>Some Imagb</imagb><file>11 KB</file><hardwa></hardwa><digiti></digiti><digita></digita><fullrs></fullrs><find>1.jp2</find><dmaccess></dmaccess><dmimage></dmimage><dmcreated>2017-01-01</dmcreated><dmmodified>2104-04-02</dmmodified><dmoclcno></dmoclcno><dmrecord>0</dmrecord><restrictionCode>1</restrictionCode><cdmfilesize>13</cdmfilesize><cdmfilesizeformatted>1.60 MB</cdmfilesizeformatted><cdmprintpdf>0</cdmprintpdf><cdmhasocr>0</cdmhasocr><cdmisnewspaper>0</cdmisnewspaper></xml>"""
    simple_object_etree = ET.fromstring(bytes(bytearray(simple_object_xmltext, encoding='utf-8')))
    return simple_object_etree


@pytest.fixture
def cpd_object_etree_fixture():
    from lxml import etree as ET
    cpd_object_filetext = """<?xml version="1.0" encoding="UTF-8"?><xml><title>Guide book of New Orleans (complete work)</title><creato></creato><contri>Stanonis, Anthony J. (Anthony Joseph)</contri><subjec>New Orleans (La.) -- Description and travel; New Orleans (La.) -- Guidebooks; New Orleans (La.) -- Tours</subjec><descri>Complete contents of a guidebook from the Louisiana State Hotel Clerks Association</descri><notes>On cover: Charter 32.....Greeters of America. Week on Sunday Mar. 12, 1916</notes><publis>Louisiana State Hotel Clerks Association</publis><date>1916-03-12</date><type>Text</type><format>jpeg</format><identi>See &#x27;reference url&#x27; on the navigational bars.</identi><source>Loyola University New Orleans Special Collections &amp; Archives, New Orleans, LA. http://library.loyno.edu/research/speccoll/</source><langua>en</langua><relati>http://louisdl.louislibraries.org/cdm/landingpage/collection/p120701coll17</relati><covera>New Orleans (La.); Vieux CarrÃ© (New Orleans, La.)</covera><coverb>1910</coverb><rights>Physical rights are held by Loyola University New Orleans. Copyright is retained in accordance with U.S. copyright law.</rights><catlog>TOG</catlog><catalo>2008-11-19</catalo><object>as010004</object><plugin></plugin><image></image><imaga></imaga><color></color><extent></extent><imagb></imagb><file></file><hardwa></hardwa><digiti></digiti><digita></digita><fullte></fullte><contac>For information or permission to use/publish, contact: mailto:archives@loyno.edu</contac><fullrs></fullrs><find>34.cpd</find><dmaccess></dmaccess><dmimage></dmimage><dmcreated>2008-11-19</dmcreated><dmmodified>2008-12-08</dmmodified><dmoclcno></dmoclcno><dmrecord>33</dmrecord><restrictionCode>1</restrictionCode><cdmfilesize>1691</cdmfilesize><cdmfilesizeformatted>0.00 MB</cdmfilesizeformatted><cdmprintpdf>0</cdmprintpdf><cdmhasocr>0</cdmhasocr><cdmisnewspaper>0</cdmisnewspaper></xml>"""
    pdfpage_etree = ET.fromstring(bytes(bytearray(cpd_object_filetext, encoding='utf-8')))
    return pdfpage_etree


@pytest.fixture
def indexfile_etree_fixture():
    from lxml import etree as ET
    pdfpage_index_filetext = """<?xml version="1.0" encoding="utf-8"?><cpd><type>Document-PDF</type><page><pagetitle>Page 1</pagetitle><pagefile>3605.pdfpage</pagefile><pageptr>3604</pageptr></page></cpd>"""
    pdfpage_etree = ET.fromstring(bytes(bytearray(pdfpage_index_filetext, encoding='utf-8')))
    return pdfpage_etree.find('.//page')


@pytest.fixture
def total_recs_etree_fixture():
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


def test_has_pdfpage_elems(indexfile_etree_fixture):
    assert scrape_cDM.has_pdfpage_elems(indexfile_etree_fixture) is True


@patch('scrape_cDM.ET')
def test_parse_binary_original_filetype(mock_ET, simple_object_etree_fixture):
    mock_ET.parse.return_value = simple_object_etree_fixture
    assert scrape_cDM.parse_binary_original_filetype('imag_path', 'imag_file') == 'jp2'
    mock_ET.parse.assert_called_with('imag_path/imag_file.xml')


@patch('scrape_cDM.ET')
def test_count_root_objects(mock_ET, total_recs_etree_fixture):
    mock_ET.parse.return_value = total_recs_etree_fixture
    scrapealias = scrape_cDM.ScrapeAlias('_')
    scrapealias.alias_dir = 'imag_alias_dir'
    assert scrapealias.count_root_objects() == 20
    mock_ET.parse.assert_called_with('imag_alias_dir/Collection_TotalRecs.xml')


@patch('scrape_cDM.ScrapeAlias.count_root_objects')
def test_calculate_chunks(mock_count_root_objects):
    scrapealias = scrape_cDM.ScrapeAlias('_')
    for total, chunksize, chunks in ((899, 100, 9),
                                     (900, 100, 10),
                                     (999, 1000, 1),
                                     (1, 1, 2), ):
        scrapealias.count_root_objects.return_value = total
        assert scrapealias.calculate_chunks(chunksize) == chunks
        mock_count_root_objects.assert_called_with()


@patch('scrape_cDM.ET')
def test_cpd_object_original_pointer_filetype(mock_ET, cpd_object_etree_fixture):
    mock_ET.parse.return_value = cpd_object_etree_fixture
    filepath, index_filename = 'imag_filepath', 'imagpointer_cpd.xml'
    assert scrape_cDM.find_cpd_object_original_pointer_filetype(filepath, index_filename) == ('33', 'jpeg')
    mock_ET.parse.assert_called_with('imag_filepath/imagpointer.xml')


@patch('scrape_cDM.CdmAPI')
def test_write_hidden_pdf_if_a_binary__xml_received_instead_of_binary(mock_API, indexfile_etree_fixture):
    binary = """<?xml version="1.0" encoding="utf-8"?><cpd><type>Document-PDF</type><page><pagetitle>Page 1</pagetitle><pagefile>3605.pdfpage</pagefile><pageptr>3604</pageptr></page></cpd>""".encode('utf-8')
    filepath, pointer, filetype = 'imag_filepath', 'imag_pointer', 'imag_filetype'
    scrapealias = scrape_cDM.ScrapeAlias('_')
    assert scrapealias.write_hidden_pdf_if_a_binary(binary, filepath, pointer, filetype) == False


# @patch('scrapt_cDM.ET')
# @patch('scrape_cDM.ScrapeAlias.find_sibling_files')
# @patch('scrape_cDM.CdmAPI')
# def test_try_to_get_a_hidden_pdf_at_root_of_cpd(mock_cDM, mock_find_sibling_files, mock_ET, cpd_object_etree_fixture, '_'):
#     mock_find_sibling_files.return_value = ['_']
#     scrapealias.find_sibling_files = mock_find_sibling_files
#     mock_etree.parse.return_value = cpd_object_etree_fixture
#     scrapealias = scrape_cDM.ScrapeAlias('_')



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
