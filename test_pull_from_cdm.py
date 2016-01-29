import unittest
import xml.etree.ElementTree as ET

from pull_from_cdm import find_pointers


class PullFromCdmTestCase(unittest.TestCase):

    mock_etree_str = """
                    <results>
                    <pager>
                      <start>1</start>
                      <maxrecs>1024</maxrecs>
                      <total>31</total>
                    </pager>
                    <records>
                    <record>
                      <collection>/p16313coll54</collection>
                      <pointer>56</pointer>
                      <filetype>jp2</filetype>
                      <parentobject>-1</parentobject>
                      <covera>See "reference url" on the navigation bar.</covera>
                      <find>57.jp2</find>
                    </record>
                    <record>
                      <collection>/p16313coll54</collection>
                      <pointer>36</pointer>
                      <filetype>jp2</filetype>
                      <parentobject>-1</parentobject>
                      <covera>See "reference url" on the navigation bar.</covera>
                      <find>37.jp2</find>
                    </record>
                    </records>
                    </results>
                    """
    mock_etree_elem = ET.fromstring(mock_etree_str)

    def setUp(self):
        self.find_pointers = find_pointers

    def tearDown(self):
        pass

    def test_find_pointers(self):
        # Setup your test

        # Exercise your System Under Test (SUT)
        pointers_list = find_pointers(self.mock_etree_elem)

        # Verify the output
        expected_pointers = ['56', '36']
        self.assertListEqual(expected_pointers, pointers_list)    

if __name__ == '__main__':
    unittest.main()
