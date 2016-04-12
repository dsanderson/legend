#include <vector>
#include <cmath>
#include <iostream>
#include <limits>

#include <nlopt.hpp>

#include "path_io.h"
#include "path_calc.h"

struct Opt_data {
  Path p1;
  Path p2;
};

double dist(Point p1, Point p2)
{
  double x = p1.x-p2.x;
  double y = p1.y-p2.y;
  double d = std::sqrt(std::pow(x,2) + std::pow(y,2));
  return d;
};

double min_dist(Point point, Path path)
{
  int len = path.size();
  double min = std::numeric_limits<double>::max();
  for(int i=0; i<len; i++)
  {
    double d = dist(point, path[i]);
    if (d<min) {
      min = d;
    }
  }
  return min;
};

double path_distance(Path p1, Path p2)
{
  int len = p1.size();
  double dis = 0.0;
  for(int i=0; i<len; i++)
  {
    double d = min_dist(p1[i],p2);
    dis += d/len;
  }
  return dis;
};

Path transform_path(const std::vector<double> &x, Path p1)
{
  //apply transforms to path for scaling purposes
  Path transformed;
  int len = p1.size();
  //const std::vector<double> x = *v;
  for (int i=0; i<len; i++)
  {
    double tmp_x = p1[i].x;
    double tmp_y = p1[i].y;
    //scale the old point
    tmp_x = tmp_x * x[3];
    tmp_y = tmp_y * x[3];
    //rotate the point
    double new_x = tmp_x*std::cos(x[2]) - tmp_y*std::sin(x[2]);
    double new_y = tmp_y*std::cos(x[2]) + tmp_x*std::sin(x[2]);
    //apply translation
    new_x += x[0];
    new_y += x[1];
    Point tmp_p;
    tmp_p.x = new_x;
    tmp_p.y = new_y;
    transformed.push_back(tmp_p);
  }
  return transformed;
};

double objective_func(const std::vector<double> &x, std::vector<double> &grad, void* f_data)
{
  Opt_data opt_data = *static_cast<Opt_data*>(f_data);
  Path transformed = transform_path(x, opt_data.p1);
  double score = path_distance(transformed, opt_data.p2);
  //calculate the score in the reverse direction, to avoid shrinking path to single point
  score += path_distance(opt_data.p2, transformed);
  return score;
};

Transform optimize_path(Path p, Path target)
{
  std::vector<double> t_form = {0,0,0,1.0};
  nlopt::opt opt(nlopt::LN_SBPLX, 4);
  //set up bounds, mostly picked at random for now
  std::vector<double> lb(4);
  lb[0] = -1.0; lb[1] = -1.0; lb[2] = -3.1416; lb[3] = 0.0;
  opt.set_lower_bounds(lb);
  std::vector<double> ub(4);
  ub[0] = 1.0; ub[1] = 1.0; ub[2] = 3.1416; ub[3] = 2.0;
  opt.set_upper_bounds(ub);

  //set up objective function, including paths
  Opt_data opt_data;
  opt_data.p1 = p;
  opt_data.p2 = target;
  opt.set_min_objective(objective_func, &opt_data);

  //set optimization end conditions
  opt.set_stopval(1e-4);
  opt.set_maxtime(1.0);

  //run optimization
  double minf;
  nlopt::result result = opt.optimize(t_form, minf);
  //std::cout << "value: " << minf << std::endl;
  //std::cout << "Path 1:" << std::endl;
  //print_path(p);
  //std::cout << "Path 2:" << std::endl;
  //print_path(target);
  //std::cout << "Path 1 transformed:" << std::endl;
  //print_path(transform_path(t_form, p));
  Transform t;
  t.tx = t_form[0];
  t.ty = t_form[1];
  t.rotation = t_form[2];
  t.scale = t_form[3];
  t.score = minf;
  return t;
};

/*int main(int argc, char const *argv[]) {
  std::cout << dist(1.0,1.0) <<std::endl;
  return 0;
}*/
