import subprocess
import os
import sys

if "SUMO_HOME" not in os.environ:
    raise Exception("You need to set the SUMO_HOME variable")
sys.path.append(os.path.join(os.environ["SUMO_HOME"], "tools"))


if __name__ == "__main__":
    script_path = os.path.join(os.environ.get("SUMO_HOME"), "tools", "randomTrips.py")
    base_path = "../sumo_project"
    output_base_path = os.path.join(base_path, "trips")
    net_file_name = "osm.net.xml.gz"
    poly_file_name = "osm.poly.xml.gz"
    bounds = [7 * 3600, 9 * 3600, 16 * 3600, 19 * 3600, 24 * 3600]
    car_intensities = [200, 700,  400, 700, 200]
    pedestrian_intensities = [200, 700, 400, 700, 200]
    intensities = [car_intensities, pedestrian_intensities]
    prefixes = ["passenger", "pedestrian"]
    vehicle_classes = ["passenger", "pedestrian"]
    min_distances = ["10.0", "0.0"]
    output_files_prefixes = ["osm.passenger", "osm.pedestrian"]

    assert len(intensities) == len(prefixes) == len(vehicle_classes) == len(min_distances) == len(output_files_prefixes)

    for i in intensities:
        assert len(i) == len(bounds)

    generated_files = []

    previous_begin_time = 0
    for i in range(len(bounds)):
        end_time = bounds[i]
        for j in range(len(intensities)):
            current_intensities = intensities[j]
            current_intensity = current_intensities[i]

            output_trip_file_path = os.path.join(output_base_path, "{}_{}.trips.xml".format(output_files_prefixes[j], i))
            output_route_file_path = os.path.join(output_base_path, "{}_{}.rou.xml".format(output_files_prefixes[j], i))
            generated_files.append(output_trip_file_path)

            args = ["python", script_path,
                    "--net-file", os.path.join(base_path, net_file_name),
                    "--additional-files", os.path.join(base_path, poly_file_name),
                    "--output-trip-file", output_trip_file_path,
                    "--route-file", output_route_file_path,
                    "--prefix", prefixes[j] + "_" + str(i),
                    "--vehicle-class", vehicle_classes[j],
                    "--min-distance", min_distances[j],
                    "--begin", str(previous_begin_time),
                    "--end", str(end_time),
                    "--insertion-rate", str(current_intensity),
                    "--validate"]

            if vehicle_classes[j] == "pedestrian":
                args.append("--pedestrian")
            else:
                args.append("--remove-loops")
            print("writing " + output_trip_file_path)
            subprocess.run(args)
