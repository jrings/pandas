# pylint: disable-msg=E1101,W0612

import nose  # noqa
import numpy as np
import pandas as pd
import pandas.util.testing as tm


class TestSparseSeriesIndexing(tm.TestCase):

    _multiprocess_can_split_ = True

    def test_loc(self):
        orig = pd.Series([1, np.nan, np.nan, 3, np.nan])
        sparse = orig.to_sparse()

        self.assertEqual(sparse.loc[0], 1)
        self.assertTrue(np.isnan(sparse.loc[1]))

        result = sparse.loc[[1, 3, 4]]
        exp = orig.loc[[1, 3, 4]].to_sparse()
        tm.assert_sp_series_equal(result, exp)

        # exceeds the bounds
        result = sparse.loc[[1, 3, 4, 5]]
        exp = orig.loc[[1, 3, 4, 5]].to_sparse()
        tm.assert_sp_series_equal(result, exp)
        # padded with NaN
        self.assertTrue(np.isnan(result[-1]))

        # dense array
        result = sparse.loc[orig % 2 == 1]
        exp = orig.loc[orig % 2 == 1].to_sparse()
        tm.assert_sp_series_equal(result, exp)

        # sparse array (actuary it coerces to normal Series)
        result = sparse.loc[sparse % 2 == 1]
        exp = orig.loc[orig % 2 == 1].to_sparse()
        tm.assert_sp_series_equal(result, exp)

    def test_loc_index(self):
        orig = pd.Series([1, np.nan, np.nan, 3, np.nan], index=list('ABCDE'))
        sparse = orig.to_sparse()

        self.assertEqual(sparse.loc['A'], 1)
        self.assertTrue(np.isnan(sparse.loc['B']))

        result = sparse.loc[['A', 'C', 'D']]
        exp = orig.loc[['A', 'C', 'D']].to_sparse()
        tm.assert_sp_series_equal(result, exp)

        # dense array
        result = sparse.loc[orig % 2 == 1]
        exp = orig.loc[orig % 2 == 1].to_sparse()
        tm.assert_sp_series_equal(result, exp)

        # sparse array (actuary it coerces to normal Series)
        result = sparse.loc[sparse % 2 == 1]
        exp = orig.loc[orig % 2 == 1].to_sparse()
        tm.assert_sp_series_equal(result, exp)

    def test_loc_slice(self):
        orig = pd.Series([1, np.nan, np.nan, 3, np.nan])
        sparse = orig.to_sparse()
        tm.assert_sp_series_equal(sparse.loc[2:], orig.loc[2:].to_sparse())

    def test_iloc(self):
        orig = pd.Series([1, np.nan, np.nan, 3, np.nan])
        sparse = orig.to_sparse()

        self.assertEqual(sparse.iloc[3], 3)
        self.assertTrue(np.isnan(sparse.iloc[2]))

        result = sparse.iloc[[1, 3, 4]]
        exp = orig.iloc[[1, 3, 4]].to_sparse()
        tm.assert_sp_series_equal(result, exp)

        with tm.assertRaises(IndexError):
            sparse.iloc[[1, 3, 5]]

    def test_iloc_slice(self):
        orig = pd.Series([1, np.nan, np.nan, 3, np.nan])
        sparse = orig.to_sparse()
        tm.assert_sp_series_equal(sparse.iloc[2:], orig.iloc[2:].to_sparse())


class TestSparseDataFrameIndexing(tm.TestCase):

    _multiprocess_can_split_ = True

    def test_loc(self):
        orig = pd.DataFrame([[1, np.nan, np.nan],
                             [2, 3, np.nan],
                             [np.nan, np.nan, 4]],
                            columns=list('xyz'))
        sparse = orig.to_sparse()

        self.assertEqual(sparse.loc[0, 'x'], 1)
        self.assertTrue(np.isnan(sparse.loc[1, 'z']))
        self.assertEqual(sparse.loc[2, 'z'], 4)

        tm.assert_sp_series_equal(sparse.loc[0], orig.loc[0].to_sparse())
        tm.assert_sp_series_equal(sparse.loc[1], orig.loc[1].to_sparse())
        tm.assert_sp_series_equal(sparse.loc[2, :],
                                  orig.loc[2, :].to_sparse())
        tm.assert_sp_series_equal(sparse.loc[2, :],
                                  orig.loc[2, :].to_sparse())
        tm.assert_sp_series_equal(sparse.loc[:, 'y'],
                                  orig.loc[:, 'y'].to_sparse())
        tm.assert_sp_series_equal(sparse.loc[:, 'y'],
                                  orig.loc[:, 'y'].to_sparse())

        result = sparse.loc[[1, 2]]
        exp = orig.loc[[1, 2]].to_sparse()
        tm.assert_sp_frame_equal(result, exp)

        result = sparse.loc[[1, 2], :]
        exp = orig.loc[[1, 2], :].to_sparse()
        tm.assert_sp_frame_equal(result, exp)

        result = sparse.loc[:, ['x', 'z']]
        exp = orig.loc[:, ['x', 'z']].to_sparse()
        tm.assert_sp_frame_equal(result, exp)

        result = sparse.loc[[0, 2], ['x', 'z']]
        exp = orig.loc[[0, 2], ['x', 'z']].to_sparse()
        tm.assert_sp_frame_equal(result, exp)

        # exceeds the bounds
        result = sparse.loc[[1, 3, 4, 5]]
        exp = orig.loc[[1, 3, 4, 5]].to_sparse()
        tm.assert_sp_frame_equal(result, exp)

        # dense array
        result = sparse.loc[orig.x % 2 == 1]
        exp = orig.loc[orig.x % 2 == 1].to_sparse()
        tm.assert_sp_frame_equal(result, exp)

        # sparse array (actuary it coerces to normal Series)
        result = sparse.loc[sparse.x % 2 == 1]
        exp = orig.loc[orig.x % 2 == 1].to_sparse()
        tm.assert_sp_frame_equal(result, exp)

    def test_loc_index(self):
        orig = pd.DataFrame([[1, np.nan, np.nan],
                             [2, 3, np.nan],
                             [np.nan, np.nan, 4]],
                            index=list('abc'), columns=list('xyz'))
        sparse = orig.to_sparse()

        self.assertEqual(sparse.loc['a', 'x'], 1)
        self.assertTrue(np.isnan(sparse.loc['b', 'z']))
        self.assertEqual(sparse.loc['c', 'z'], 4)

        tm.assert_sp_series_equal(sparse.loc['a'], orig.loc['a'].to_sparse())
        tm.assert_sp_series_equal(sparse.loc['b'], orig.loc['b'].to_sparse())
        tm.assert_sp_series_equal(sparse.loc['b', :],
                                  orig.loc['b', :].to_sparse())
        tm.assert_sp_series_equal(sparse.loc['b', :],
                                  orig.loc['b', :].to_sparse())

        tm.assert_sp_series_equal(sparse.loc[:, 'z'],
                                  orig.loc[:, 'z'].to_sparse())
        tm.assert_sp_series_equal(sparse.loc[:, 'z'],
                                  orig.loc[:, 'z'].to_sparse())

        result = sparse.loc[['a', 'b']]
        exp = orig.loc[['a', 'b']].to_sparse()
        tm.assert_sp_frame_equal(result, exp)

        result = sparse.loc[['a', 'b'], :]
        exp = orig.loc[['a', 'b'], :].to_sparse()
        tm.assert_sp_frame_equal(result, exp)

        result = sparse.loc[:, ['x', 'z']]
        exp = orig.loc[:, ['x', 'z']].to_sparse()
        tm.assert_sp_frame_equal(result, exp)

        result = sparse.loc[['c', 'a'], ['x', 'z']]
        exp = orig.loc[['c', 'a'], ['x', 'z']].to_sparse()
        tm.assert_sp_frame_equal(result, exp)

        # dense array
        result = sparse.loc[orig.x % 2 == 1]
        exp = orig.loc[orig.x % 2 == 1].to_sparse()
        tm.assert_sp_frame_equal(result, exp)

        # sparse array (actuary it coerces to normal Series)
        result = sparse.loc[sparse.x % 2 == 1]
        exp = orig.loc[orig.x % 2 == 1].to_sparse()
        tm.assert_sp_frame_equal(result, exp)

    def test_loc_slice(self):
        orig = pd.DataFrame([[1, np.nan, np.nan],
                             [2, 3, np.nan],
                             [np.nan, np.nan, 4]],
                            columns=list('xyz'))
        sparse = orig.to_sparse()
        tm.assert_sp_frame_equal(sparse.loc[2:], orig.loc[2:].to_sparse())

    def test_iloc(self):
        orig = pd.DataFrame([[1, np.nan, np.nan],
                             [2, 3, np.nan],
                             [np.nan, np.nan, 4]])
        sparse = orig.to_sparse()

        self.assertEqual(sparse.iloc[1, 1], 3)
        self.assertTrue(np.isnan(sparse.iloc[2, 0]))

        tm.assert_sp_series_equal(sparse.iloc[0], orig.loc[0].to_sparse())
        tm.assert_sp_series_equal(sparse.iloc[1], orig.loc[1].to_sparse())
        tm.assert_sp_series_equal(sparse.iloc[2, :],
                                  orig.iloc[2, :].to_sparse())
        tm.assert_sp_series_equal(sparse.iloc[2, :],
                                  orig.iloc[2, :].to_sparse())
        tm.assert_sp_series_equal(sparse.iloc[:, 1],
                                  orig.iloc[:, 1].to_sparse())
        tm.assert_sp_series_equal(sparse.iloc[:, 1],
                                  orig.iloc[:, 1].to_sparse())

        result = sparse.iloc[[1, 2]]
        exp = orig.iloc[[1, 2]].to_sparse()
        tm.assert_sp_frame_equal(result, exp)

        result = sparse.iloc[[1, 2], :]
        exp = orig.iloc[[1, 2], :].to_sparse()
        tm.assert_sp_frame_equal(result, exp)

        result = sparse.iloc[:, [1, 0]]
        exp = orig.iloc[:, [1, 0]].to_sparse()
        tm.assert_sp_frame_equal(result, exp)

        result = sparse.iloc[[2], [1, 0]]
        exp = orig.iloc[[2], [1, 0]].to_sparse()
        tm.assert_sp_frame_equal(result, exp)

        with tm.assertRaises(IndexError):
            sparse.iloc[[1, 3, 5]]

    def test_iloc_slice(self):
        orig = pd.DataFrame([[1, np.nan, np.nan],
                             [2, 3, np.nan],
                             [np.nan, np.nan, 4]],
                            columns=list('xyz'))
        sparse = orig.to_sparse()
        tm.assert_sp_frame_equal(sparse.iloc[2:], orig.iloc[2:].to_sparse())
