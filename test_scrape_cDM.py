#! /usr/bin/python3

import os

import pytest
import mock
import scrape_cDM


# run pytest from project root with `pytest`

def test_is_it_a_404_xml():
    error_return_text = """<?xml version="1.0" encoding="UTF-8"?>
<error><code>-2</code><message>Requested item not found</message><restrictionCode>-1</restrictionCode>
</error>"""
    assert scrape_cDM.is_it_a_404_xml(error_return_text) is True


def test_is_it_a_404_json():
    error_return_text = """{"code":"-2","message":"Requested item not found","restrictionCode":"-1"}"""
    assert scrape_cDM.is_it_a_404_json(error_return_text) is True


@pytest.fixture
def make_pdfpage_xml():
    from lxml import etree as ET
    pdfpage_index_filetext = """<?xml version="1.0" encoding="utf-8"?>
<cpd>
  <type>Document-PDF</type>
  <page>
    <pagetitle>Page 1</pagetitle>
    <pagefile>3605.pdfpage</pagefile>
    <pageptr>3604</pageptr>
  </page>
</cpd>"""
    pdfpage_etree = ET.fromstring(bytes(bytearray(pdfpage_index_filetext,
                                                  encoding='utf-8')))
    return pdfpage_etree.find('.//page')

def test_has_pdfpage_elems(make_pdfpage_xml):
    assert scrape_cDM.has_pdfpage_elems(make_pdfpage_xml) is True


def test_parse_binary_original_filetype():
    fake_filepath = os.path.join('.', 'Test_Files')
    assert scrape_cDM.parse_binary_original_filetype(fake_filepath, 'Simple_Object') == 'jpg'


def test_count_root_objects():
    instance = scrape_cDM.ScrapeAlias('_')
    instance.alias_dir = 'Test_Files'
    assert instance.count_root_objects() == 456
