#ifndef PATHS_PATH_CALC_H
#define PATHS_PATH_CALC_H

struct Transform {
  double tx;
  double ty;
  double rotation;
  double scale;
};

double dist(double x, double y);

double path_distance(Path p1, Path p2);

void optimize_path(Path p, Path target);

#endif
