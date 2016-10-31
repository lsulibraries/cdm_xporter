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
def binary_decodes_fixture():
    class Binary():
        def decode(self, *args, **kwargs):
            return True
    return Binary()


@pytest.fixture
def binary_doesnt_decode_fixture():
    class Binary():
        def decode(self, *args, **kwargs):
            raise UnicodeDecodeError('imag', b"", 42, 43, 'imag_exception occurredd')
    return Binary()


@pytest.fixture
def ETparse_fixture(*args, **kwargs):
    class ImagParse():
        def findall(*args, **kwargs):
            return 'imag_children_pointers_list'
        def assert_called_with(*args, **kwargs):
            return (args, kwargs)
    return ImagParse


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


@patch('scrape_cDM.CdmAPI.write_binary_to_file')
def test_write_hidden_pdf_if_a_binary__xml_received_instead_of_binary_failure(mock_API, binary_decodes_fixture):
    # binary = """<?xml version="1.0" encoding="utf-8"?><cpd><type>Document-PDF</type><page><pagetitle>Page 1</pagetitle><pagefile>3605.pdfpage</pagefile><pageptr>3604</pageptr></page></cpd>""".encode('utf-8')
    filepath, pointer, filetype = 'imag_filepath', 'imag_pointer', 'imag_filetype'
    scrapealias = scrape_cDM.ScrapeAlias('_')
    assert scrapealias.write_hidden_pdf_if_a_binary(binary_decodes_fixture, filepath, pointer, filetype) is False


@patch('scrape_cDM.CdmAPI.write_binary_to_file')
def test_write_hidden_pdf_if_a_binary__xml_received_instead_of_binary_success(mock_API, binary_doesnt_decode_fixture):
    # binary = """<?xml version="1.0" encoding="utf-8"?><cpd><type>Document-PDF</type><page><pagetitle>Page 1</pagetitle><pagefile>3605.pdfpage</pagefile><pageptr>3604</pageptr></page></cpd>""".encode('utf-8')
    filepath, pointer, filetype = 'imag_filepath', 'imag_pointer', 'imag_filetype'
    scrapealias = scrape_cDM.ScrapeAlias('_')
    assert scrapealias.write_hidden_pdf_if_a_binary(binary_doesnt_decode_fixture, filepath, pointer, filetype) is True
    mock_API.assert_called_with(binary_doesnt_decode_fixture, 'imag_filepath', 'imag_pointer', 'imag_filetype')


def test_find_sibling_files():
    scrapealias = scrape_cDM.ScrapeAlias('_')
    scrapealias.tree_snapshot = [['imag_a', ['imagd_1'], ['a1', 'a2', 'a3']], [['imag_b'], [], ['b1', 'b2']], [['imag_c'], [], ['c1', 'c2', 'c3', 'c4']]]
    assert set(scrapealias.find_sibling_files('a1')) == {'a1', 'a2', 'a3'}
    assert set(scrapealias.find_sibling_files('b2')) == {'b1', 'b2'}
    assert set(scrapealias.find_sibling_files('c3')) == {'c1', 'c2', 'c3', 'c4'}


@patch('scrape_cDM.ScrapeAlias.write_hidden_pdf_if_a_binary')
@patch('scrape_cDM.ScrapeAlias.try_getting_hidden_pdf')
@patch('scrape_cDM.ScrapeAlias.find_sibling_files')
@patch('scrape_cDM.find_cpd_object_original_pointer_filetype')
def test_try_to_get_a_hidden_pdf_at_root_of_cpd(mock_findcpd, mock_findsibl, mock_tryhidden, mock_writehidden):
    # if binary already on disk.
    scrapealias = scrape_cDM.ScrapeAlias('_')
    scrapealias.alias_dir = 'fake/filepath'
    scrapealias.find_sibling_files = mock_findsibl
    scrapealias.try_getting_hidden_pdf = mock_tryhidden
    scrapealias.write_hidden_pdf_if_a_binary = mock_writehidden
    mock_findcpd.return_value = ('imag1', 'img')
    mock_findsibl.return_value = ['imag1.img', 'imag2.img', 'imag3.img']
    scrapealias.try_to_get_a_hidden_pdf_at_root_of_cpd('fakefile')
    mock_findcpd.assert_called_with('fake/filepath/Cpd', 'fakefile')
    mock_findsibl.assert_called_with('fakefile')
    assert not mock_tryhidden.called
    assert not mock_writehidden.called

    # if binary not already on disk
    scrapealias = scrape_cDM.ScrapeAlias('_')
    scrapealias.alias_dir = 'fake/filepath'
    scrapealias.find_sibling_files = mock_findsibl
    scrapealias.try_getting_hidden_pdf = mock_tryhidden
    scrapealias.write_hidden_pdf_if_a_binary = mock_writehidden
    mock_findcpd.return_value = ('imag1', 'other')
    mock_findsibl.return_value = ['imag1.img', 'imag2.img', 'imag3.img']
    mock_tryhidden.return_value = 'imag_binary'
    scrapealias.try_to_get_a_hidden_pdf_at_root_of_cpd('fakefile')
    mock_findcpd.assert_called_with('fake/filepath/Cpd', 'fakefile')
    mock_findsibl.assert_called_with('fakefile')
    mock_tryhidden.assert_called_with('imag1', 'other')
    mock_writehidden.assert_called_with('imag_binary', 'fake/filepath/Cpd', 'imag1', 'other')


@patch('scrape_cDM.ScrapeAlias.do_collection_level_metadata')
@patch('scrape_cDM.ScrapeAlias.do_root_level_objects')
@patch('scrape_cDM.ScrapeAlias.do_compound_objects')
def test_main_loop(mock_docpd, mock_doroot, mock_docoll):
    scrapealias = scrape_cDM.ScrapeAlias('_')
    scrapealias.do_collection_level_metadata = mock_docoll
    scrapealias.do_root_level_objects = mock_doroot
    scrapealias.do_compound_objects = mock_docpd
    assert not mock_docoll.called
    assert not mock_doroot.called
    assert not mock_docpd.called
    scrapealias.main()
    mock_docoll.assert_called_with()
    mock_doroot.assert_called_with()
    mock_docpd.assert_called_with()


@patch('scrape_cDM.os')
@patch('scrape_cDM.CdmAPI')
def test_do_collection_level_metadata(mock_API, mock_os):
    mock_os.makedirs.return_value = True
    mock_API.retrieve_collection_total_recs.return_value = 'total_recs'
    mock_API.retrieve_collection_metadata.return_value = 'coll_metadata'
    mock_API.retrieve_collection_fields_json.return_value = 'fields_json'
    mock_API.retrieve_collecion_fields_xml.return_value = 'fields_xml'
    scrapealias = scrape_cDM.ScrapeAlias('imag_alias')
    scrapealias.alias_dir = 'imag_filepath'

    mock_os.listdir.return_value = ('Collection_TotalRecs.xml', 'Collection_Metadata.xml', 'Collection_Fields.json', 'Collection_Fields.xml')
    scrapealias.do_collection_level_metadata()
    assert not mock_API.retrieve_collection_total_recs.called
    assert not mock_API.retrieve_collection_metadata.called
    assert not mock_API.retrieve_collection_fields_json.called
    assert not mock_API.retrieve_collection_fields_xml.called

    mock_os.listdir.return_value = ('')
    scrapealias.do_collection_level_metadata()
    mock_API.retrieve_collection_total_recs.assert_called_with('imag_alias')
    mock_API.retrieve_collection_metadata.assert_called_with('imag_alias')
    mock_API.retrieve_collection_fields_json.assert_called_with('imag_alias')
    mock_API.retrieve_collection_fields_xml.assert_called_with('imag_alias')
    fake_json_fields_call = mock_API.retrieve_collection_fields_json('imag_alias')
    fake_xml_fields_call = mock_API.retrieve_collection_fields_xml('imag_alias')
    assert mock_API.write_xml_to_file.call_count == 3
    assert mock_API.write_json_to_file.call_count == 1
    mock_API.write_json_to_file.assert_called_with(fake_json_fields_call, 'imag_filepath', 'Collection_Fields')
    mock_API.write_xml_to_file.assert_called_with(fake_xml_fields_call, 'imag_filepath', 'Collection_Fields')
    # only the last call to each mock_API.fn seems to be recorded, so here we just test the last call to each fn.


@patch('scrape_cDM.CdmAPI')
def test_try_getting_hidden_pdf(mock_API):
    scrapealias = scrape_cDM.ScrapeAlias('imag_alias')
    import urllib
    mock_API.retrieve_binary.return_value = 'actual_imag_binary'
    assert scrapealias.try_getting_hidden_pdf('imag_pointer', 'imag_filetype') == 'actual_imag_binary'
    assert scrapealias.unavailable_binaries == set()
    mock_API.retrieve_binary.side_effect = urllib.error.HTTPError('imag', b"", 42, 43, 'imag_exception occurredd')
    assert scrapealias.try_getting_hidden_pdf('imag_pointer', 'imag_filetype') is False
    assert scrapealias.unavailable_binaries == {('imag_pointer', 'imag_filetype'), }


@patch('scrape_cDM.has_pdfpage_elems')
@patch('scrape_cDM.ScrapeAlias.try_to_get_a_hidden_pdf_at_root_of_cpd')
def test_are_child_pointers_pdfpages(mock_try_to_get, mock_has_pdfpage):
    scrapealias = scrape_cDM.ScrapeAlias('_')
    scrapealias.try_to_get_a_hidden_pdf_at_root_of_cpd = mock_try_to_get
    # scrape_cDM.has_pdfpage_elems = mock_has_pdfpage
    mock_has_pdfpage.return_value = False
    assert scrapealias.are_child_pointers_pdfpages('imag_list', 'imag_filename') is True
    mock_has_pdfpage.assert_called_with('imag_list')
    assert not mock_try_to_get.called
    mock_has_pdfpage.return_value = True
    mock_try_to_get.return_value = False
    assert scrapealias.are_child_pointers_pdfpages('imag_list', 'imag_filename') is False
    mock_has_pdfpage.assert_called_with('imag_list')
    mock_try_to_get.assert_called_with('imag_filename')
    mock_has_pdfpage.return_value = True
    mock_try_to_get.return_value = True
    assert scrapealias.are_child_pointers_pdfpages('imag_list', 'imag_filename') is False
    mock_has_pdfpage.assert_called_with('imag_list')
    mock_try_to_get.assert_called_with('imag_filename')


@patch('scrape_cDM.ET.parse')
@patch('scrape_cDM.ScrapeAlias.are_child_pointers_pdfpages')
def test_parse_children_of_cpd(mock_arepointers, mock_ETparse, ETparse_fixture):
    scrapealias = scrape_cDM.ScrapeAlias('_')
    scrapealias.alias_dir = 'imag_dir'
    scrapealias.are_child_pointers_pdfpages = mock_arepointers
    scrape_cDM.ET.parse = mock_ETparse
    mock_ETparse.return_value = ETparse_fixture
    mock_ETparse.findall = ETparse_fixture
    mock_arepointers.return_value = False
    assert scrapealias.parse_children_of_cpd('imag_parent') is None
    mock_ETparse.assert_called_with('imag_dir/Cpd/imag_parent_cpd.xml')
    mock_ETparse.findall.assert_called_with('imag_elem', 'imag_parent_cpd.xml')
    mock_arepointers.return_value = True
    assert scrapealias.parse_children_of_cpd('imag_parent') == 'imag_children_pointers_list'
