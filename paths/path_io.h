#ifndef PATHS_PATH_IO_H
#define PATHS_PATH_IO_H

struct Point {
  double x;
  double y;
};

typedef std::vector<Point> Path;

Path import_path(std::string filename);

std::vector<std::string> import_path_filenames(std::string filename);

std::vector<Path> import_paths(std::vector<std::string> path_filenames);

void print_path(Path path);

#endif
