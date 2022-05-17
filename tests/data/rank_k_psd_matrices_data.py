import random

import geomstats.backend as gs
from geomstats.geometry.rank_k_psd_matrices import BuresWassersteinBundle, PSDMatrices
from tests.data_generation import (
    _FiberBundleTestData,
    _ManifoldTestData,
    _QuotientMetricTestData,
)


class PSDMatricesTestData(_ManifoldTestData):
    n_list = random.sample(range(3, 5), 2)
    k_list = n_list
    space_args_list = list(zip(n_list, k_list))
    shape_list = [(n, n) for n in n_list]
    n_points_list = random.sample(range(2, 5), 2)
    n_vecs_list = random.sample(range(2, 5), 2)

    space = PSDMatrices

    def belongs_test_data(self):
        smoke_data = [
            dict(
                n=3,
                k=2,
                mat=[
                    [0.8369314, -0.7342977, 1.0402943],
                    [0.04035992, -0.7218659, 1.0794858],
                    [0.9032698, -0.73601735, -0.36105633],
                ],
                expected=False,
            ),
            dict(
                n=3,
                k=2,
                mat=[[1.0, 1.0, 0], [1.0, 4.0, 0], [0, 0, 0]],
                expected=True,
            ),
        ]
        return self.generate_tests(smoke_data)


class BuresWassersteinBundleTestData(_FiberBundleTestData):
    n_list = random.sample(range(3, 5), 2)
    k_list = [n - 1 for n in n_list]
    space_args_list = list(zip(n_list, k_list))
    shape_list = [(n, n) for n in n_list]
    n_points_list = random.sample(range(1, 5), 2) * 2
    n_base_points_list = [1] * len(n_points_list) + n_points_list
    n_vecs_list = random.sample(range(1, 5), 2)

    base = PSDMatrices
    space = BuresWassersteinBundle


class TestDataPSDMetricBuresWasserstein(_QuotientMetricTestData):
    n_list = random.sample(range(3, 8), 5)
    metric_args_list = [(n, n - 1) for n in n_list]
    shape_list = [(n, n) for n in n_list]
    space_list = [PSDMatrices(n, n - 1) for n in n_list]
    bundle_list = [BuresWassersteinBundle(n, n - 1) for n in n_list]
    n_points_list = random.sample(range(1, 7), 5)
    n_samples_list = random.sample(range(1, 7), 5)
    n_points_a_list = random.sample(range(1, 7), 5)
    n_tangent_vecs_list = random.sample(range(1, 7), 3)
    n_points_b_list = [1]
    batch_size_list = random.sample(range(2, 7), 5)
    alpha_list = [1] * 5
    n_rungs_list = [1] * 5
    scheme_list = ["pole"] * 5

    def inner_product_data(self):
        smoke_data = [
            dict(
                n=3,
                tangent_vec_a=[[2.0, 1.0, 1.0], [1.0, 0.5, 0.5], [1.0, 0.5, 0.5]],
                tangent_vec_b=[[1.0, 2.0, 4.0], [2.0, 3.0, 8.0], [4.0, 8.0, 5.0]],
                base_point=[[1.0, 0.0, 0.0], [0.0, 1.5, 0.5], [0.0, 0.5, 1.5]],
                expected=4.0,
            )
        ]
        return self.generate_tests(smoke_data)

    def exp_test_data(self):
        smoke_data = [
            dict(
                n=2,
                tangent_vec=[[2.0, 0.0], [0.0, 2.0]],
                base_point=[[1.0, 0.0], [0.0, 1.0]],
                expected=[[4.0, 0.0], [0.0, 4.0]],
            )
        ]
        return self.generate_tests(smoke_data)

    def log_test_data(self):
        smoke_data = [
            dict(
                n=2,
                point=[[4.0, 0.0], [0.0, 4.0]],
                base_point=[[1.0, 0.0], [0.0, 1.0]],
                expected=[[2.0, 0.0], [0.0, 2.0]],
            )
        ]
        return self.generate_tests(smoke_data)

    def squared_dist_test_data(self):
        smoke_data = [
            dict(
                n=2,
                point_a=[[1.0, 0.0], [0.0, 1.0]],
                point_b=[[2.0, 0.0], [0.0, 2.0]],
                expected=2 + 4 - (2 * 2 * 2**0.5),
            )
        ]
        return self.generate_tests(smoke_data)

    def exp_shape_test_data(self):
        return self._exp_shape_test_data(
            self.metric_args_list,
            self.space_list,
            self.shape_list,
        )

    def log_shape_test_data(self):
        return self._log_shape_test_data(
            self.metric_args_list,
            self.space_list,
        )

    def dist_is_norm_of_log_test_data(self):
        return self._dist_is_norm_of_log_test_data(
            self.metric_args_list,
            self.space_list,
            self.n_points_a_list,
            self.n_points_b_list,
            rtol=gs.rtol,
            atol=gs.atol,
        )

    def dist_is_positive_test_data(self):
        return self._dist_is_positive_test_data(
            self.metric_args_list,
            self.space_list,
            self.n_points_a_list,
            self.n_points_b_list,
            is_positive_atol=gs.atol,
        )

    def dist_is_symmetric_test_data(self):
        return self._dist_is_symmetric_test_data(
            self.metric_args_list,
            self.space_list,
            self.n_points_a_list,
            self.n_points_b_list,
            atol=gs.atol * 1000,
        )

    def dist_point_to_itself_is_zero_test_data(self):
        return self._dist_point_to_itself_is_zero_test_data(
            self.metric_args_list,
            self.space_list,
            self.n_points_a_list,
            atol=gs.atol * 10,
        )

    def inner_product_is_symmetric_test_data(self):
        return self._inner_product_is_symmetric_test_data(
            self.metric_args_list,
            self.space_list,
            self.shape_list,
            self.n_tangent_vecs_list,
            rtol=gs.rtol,
            atol=gs.atol,
        )

    def squared_dist_is_positive_test_data(self):
        return self._squared_dist_is_positive_test_data(
            self.metric_args_list,
            self.space_list,
            self.n_points_a_list,
            self.n_points_b_list,
            is_positive_atol=gs.atol,
        )

    def squared_dist_is_symmetric_test_data(self):
        return self._squared_dist_is_symmetric_test_data(
            self.metric_args_list,
            self.space_list,
            self.n_points_a_list,
            self.n_points_b_list,
            atol=gs.atol,
        )

    def exp_belongs_test_data(self):
        return self._exp_belongs_test_data(
            self.metric_args_list,
            self.space_list,
            self.shape_list,
            self.n_samples_list,
            belongs_atol=gs.atol * 1000,
        )

    def log_is_tangent_test_data(self):
        return self._log_is_tangent_test_data(
            self.metric_args_list,
            self.space_list,
            self.n_samples_list,
            is_tangent_atol=gs.atol * 1000,
        )

    def geodesic_ivp_belongs_test_data(self):
        return self._geodesic_ivp_belongs_test_data(
            self.metric_args_list,
            self.space_list,
            self.shape_list,
            self.n_points_list,
            belongs_atol=gs.atol * 1000,
        )

    def geodesic_bvp_belongs_test_data(self):
        return self._geodesic_bvp_belongs_test_data(
            self.metric_args_list,
            self.space_list,
            self.n_points_list,
            belongs_atol=gs.atol * 1000,
        )

    def exp_after_log_test_data(self):
        return self._exp_after_log_test_data(
            self.metric_args_list,
            self.space_list,
            self.n_samples_list,
            rtol=gs.rtol * 100,
            atol=gs.atol * 10000,
        )

    def log_after_exp_test_data(self):
        return self._log_after_exp_test_data(
            self.metric_args_list,
            self.space_list,
            self.shape_list,
            self.n_samples_list,
            rtol=gs.rtol * 100,
            atol=gs.atol * 10000,
        )

    def exp_ladder_parallel_transport_test_data(self):
        return self._exp_ladder_parallel_transport_test_data(
            self.metric_args_list,
            self.space_list,
            self.shape_list,
            self.n_samples_list,
            self.n_rungs_list,
            self.alpha_list,
            self.scheme_list,
        )

    def exp_geodesic_ivp_test_data(self):
        return self._exp_geodesic_ivp_test_data(
            self.metric_args_list,
            self.space_list,
            self.shape_list,
            self.n_samples_list,
            self.n_points_list,
            rtol=gs.rtol,
            atol=gs.atol,
        )

    def parallel_transport_ivp_is_isometry_test_data(self):
        return self._parallel_transport_ivp_is_isometry_test_data(
            self.metric_args_list,
            self.space_list,
            self.shape_list,
            self.n_samples_list,
            is_tangent_atol=gs.atol * 1000,
            atol=gs.atol * 1000,
        )

    def parallel_transport_bvp_is_isometry_test_data(self):
        return self._parallel_transport_bvp_is_isometry_test_data(
            self.metric_args_list,
            self.space_list,
            self.shape_list,
            self.n_samples_list,
            is_tangent_atol=gs.atol * 1000,
            atol=gs.atol * 1000,
        )

    def triangle_inequality_of_dist_test_data(self):
        return self._triangle_inequality_of_dist_test_data(
            self.metric_args_list, self.space_list, self.n_points_list
        )

    def dist_is_smaller_than_bundle_dist_test_data(self):
        return self._dist_is_smaller_than_bundle_dist_test_data(
            self.metric_args_list, self.bundle_list, self.n_points_list
        )

    def log_is_horizontal_test_data(self):
        return self._log_is_horizontal_test_data(
            self.metric_args_list, self.bundle_list, self.n_points_list
        )
