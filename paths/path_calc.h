#ifndef PATHS_PATH_CALC_H
#define PATHS_PATH_CALC_H

struct Transform {
  double tx;
  double ty;
  double rotation;
  double scale;
  double score = -1.0;
};

double dist(double x, double y);

double path_distance(Path p1, Path p2);

Path transform_path(const std::vector<double> &x, Path p1);

Transform optimize_path(Path p, Path target);

#endif
