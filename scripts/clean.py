import os
import argparse

from lxml import etree

def get_gpx_filename(tcx_file):
    directory = os.path.dirname(tcx_file)
    base_name = os.path.splitext(os.path.basename(tcx_file))[0]
    filename = f"{base_name}.gpx"
    return os.path.join(directory, filename)

def clean_xml(file_path):
    with open(file_path, 'rb') as file:
        content = file.read().lstrip()  # Remove any leading whitespace or BOM
    return content

def convert_tcx_to_gpx(tcx_file):
    cleaned_xml = clean_xml(tcx_file)
    
    root = etree.fromstring(cleaned_xml)
    gpx = etree.Element("gpx", version="1.1", creator="tcx2gpx")

    has_track = False
    for activity in root.findall('.//{*}Activity'):
        for lap in activity.findall('.//{*}Lap'):
            for track in lap.findall('.//{*}Track'):
                # Avoid inserting multiple tracks
                if has_track:
                    break
                 
                for trackpoint in track.findall('.//{*}Trackpoint'):
                    if not has_track:
                        gpx_track = etree.SubElement(gpx, "trk")
                        
                        sport = activity.get('Sport').lower()
                        type_elem = etree.SubElement(gpx_track, 'type')
                        type_elem.text = sport
                        
                        gpx_segment = etree.SubElement(gpx_track, "trkseg")
                        has_track = True

                    gpx_trackpoint = etree.SubElement(gpx_segment, "trkpt")

                    time = trackpoint.find('.//{*}Time')
                    if time is not None:
                        time_elem = etree.SubElement(gpx_trackpoint, "time")
                        time_elem.text = time.text

                    hr = trackpoint.find('.//{*}HeartRateBpm/{*}Value')
                    if hr is not None:
                        extensions = etree.SubElement(gpx_trackpoint, "extensions")
                        hr_elem = etree.SubElement(extensions, "hr")
                        hr_elem.text = str(hr.text)

    gpx_file = get_gpx_filename(tcx_file)
    with open(gpx_file, "wb") as gpx_out:
        gpx_out.write(etree.tostring(gpx, pretty_print=True, xml_declaration=True, encoding="UTF-8"))

def main():
    parser = argparse.ArgumentParser(description="Convert TCX file to GPX format.")
    parser.add_argument("tcx", help="Input TCX file")
    args = parser.parse_args()

    convert_tcx_to_gpx(args.tcx)

if __name__ == "__main__":
    main()