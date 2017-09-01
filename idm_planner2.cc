#include "drake/automotive/idm_planner2.h"

#include <cmath>

#include "drake/common/autodiff_overloads.h"
#include "drake/common/drake_assert.h"
#include "drake/common/symbolic_formula.h"

namespace drake {
namespace automotive {
bool flag = true;
int count = 0;
template <typename T>
const T IdmPlanner2<T>::Evaluate(const IdmPlannerParameters<T>& params,
                                const T& ego_velocity, const T& target_distance,
                                const T& target_distance_dot) {
  DRAKE_DEMAND(params.IsValid());

  using std::pow;
  using std::sqrt;

  const T& v_ref = params.v_ref();
  const T& a = params.a();
  const T& b = params.b();
  const T& s_0 = params.s_0();
  const T& time_headway = params.time_headway();
  const T& delta = params.delta();

  DRAKE_DEMAND(a > 0.);
  DRAKE_DEMAND(b > 0.);
  DRAKE_DEMAND(target_distance > 0.);

  // Compute the interaction acceleration terms.
  const T& closing_term =
      ego_velocity * target_distance_dot / (2 * sqrt(a * b));
  const T& too_close_term = s_0 + ego_velocity * time_headway;
  const T& accel_interaction =
      pow((closing_term + too_close_term) / target_distance, 2.);

  // Compute the free-road acceleration term.
  const T& accel_free_road = pow(ego_velocity / v_ref, delta);

  // Compute the resultant acceleration (IDM equation).

  T fin = a * (1. - accel_free_road - accel_interaction); //////////////////
  if(ego_velocity > 1 && flag)
    fin = -0.05;
  else
  {
    fin = 0;
    flag = false;
  }

  if(flag == false)
  {
    fin = 0.3;
  }

  return fin;
}

// These instantiations must match the API documentation in idm_planner.h.
template class IdmPlanner2<double>;
template class IdmPlanner2<drake::AutoDiffXd>;
template class IdmPlanner2<drake::symbolic::Expression>;

}  // namespace automotive
}  // namespace drake
