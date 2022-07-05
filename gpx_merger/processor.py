#!/usr/bin/python

import os
import fileinput
import shutil
import file_sorter

input_directory = "input"
output_directory = "output"
output_filename = "Combined.gpx"

def clearMetadata():
    os.chdir(input_directory)
    for filename in file_sorter.sortByNameWithExtension("*.gpx"):
        with open(filename, 'r') as file:
            file_name = os.path.splitext(filename)[0]
            header_end_index = 0
            footer_begin_index = 0
            content = file.read().split('\n')
            with open("%s_output.gpxTemp"%file_name, 'w') as output_file:
                for index, line in enumerate(content):
                    if '<trkseg>' in line and header_end_index == 0:
                        header_end_index = index
                    if '</trk>' in line:
                        footer_begin_index = index
                    line = line+'\n'
                    content[index] = line
                output_file.writelines(content[header_end_index:footer_begin_index])

def mergeContent():
    input_files = file_sorter.sortByNameWithExtension("*.gpxTemp")
    input_lines = fileinput.input(input_files)

    os.chdir('../')

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    elif os.path.exists("%s/%s"%(output_directory, output_filename)):
        os.remove("%s/%s"%(output_directory, output_filename))

    os.chdir(input_directory)

    with open(output_filename, 'w') as outputFile:
        outputFile.writelines(input_lines)
        shutil.move(output_filename, '../'+output_directory)
    
    for file in input_files:
        os.remove(file)

def addMetadata():
    os.chdir('../'+output_directory)
    with open(output_filename, 'r') as input_file:
        with open("temp.gpx", 'w') as output_file:
            header_lines = ['<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n', '<gpx version=\"1.1\" creator=\"Eren Kabakci\"><metadata><name>2022 Summer Roadtrip</name>\n', '</metadata>\n', '<trk><name>2022 Summer Roadtrip</name>\n']
            footer_lines = ['</trk>\n', '</gpx>']
            output_file.writelines(header_lines)
            output_file.write(input_file.read())
            output_file.writelines(footer_lines)
            os.replace("temp.gpx", output_filename)
    os.chdir("..")
