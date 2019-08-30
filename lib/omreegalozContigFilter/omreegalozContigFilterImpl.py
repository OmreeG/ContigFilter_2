# -*- coding: utf-8 -*-
#BEGIN_HEADER
# The header block is where all import statments should live
import logging
import os
from pprint import pformat


#other imports
from Bio import SeqIO

from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.KBaseReportClient import KBaseReport
#END_HEADER


class omreegalozContigFilter:
    '''
    Module Name:
    omreegalozContigFilter

    Module Description:
    A KBase module: omreegalozContigFilter
This sample module contains one small method that filters contigs.
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/OmreeG/ContigFilter_2.git"
    GIT_COMMIT_HASH = "7a94d42f93492b940db9bd42410348f7392c557d"

    #BEGIN_CLASS_HEADER
    # Class variables and functions can be defined in this block
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        
        # Any configuration parameters that are important should be parsed and
        # saved in the constructor.
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_omreegalozContigFilter(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_omreegalozContigFilter

        # Print statements to stdout/stderr are captured and available as the App log
        logging.info('Starting run_omreegalozContigFilter function. Params=' + pformat(params))

        # Step 1 - Parse/examine the parameters and catch any errors
        # It is important to check that parameters exist and are defined, and that nice error
        # messages are returned to users.  Parameter values go through basic validation when
        # defined in a Narrative App, but advanced users or other SDK developers can call
        # this function directly, so validation is still important.
        logging.info('Validating parameters.')
        if 'workspace_name' not in params:
            raise ValueError('Parameter workspace_name is not set in input arguments')
        workspace_name = params['workspace_name']
        #DEBUG:
        print("HELLO WE ARE HERE")
        if 'assembly_input_ref' not in params:
            print(params)
            raise ValueError('Parameter assembly_input_ref is not set in input arguments')
        assembly_input_ref = params['assembly_input_ref']
        if 'min_length' not in params:
            raise ValueError('Parameter min_length is not set in input arguments')
        min_length_orig = params['min_length']
        min_length = None
        try:
            min_length = int(min_length_orig)
        except ValueError:
            raise ValueError('Cannot parse integer from min_length parameter (' + str(min_length_orig) + ')')
        if min_length < 0:
            raise ValueError('min_length parameter cannot be negative (' + str(min_length) + ')')


        # Step 2 - Download the input data as a Fasta and
        # We can use the AssemblyUtils module to download a FASTA file from our Assembly data object.
        # The return object gives us the path to the file that was created.
        logging.info('Downloading Assembly data as a Fasta file.')
        assemblyUtil = AssemblyUtil(self.callback_url)
        fasta_file = assemblyUtil.get_assembly_as_fasta({'ref': assembly_input_ref})


        # Step 3 - Actually perform the filter operation, saving the good contigs to a new fasta file.
        # We can use BioPython to parse the Fasta file and build and save the output to a file.
        good_contigs = []
        n_total = 0
        n_remaining = 0
        for record in SeqIO.parse(fasta_file['path'], 'fasta'):
            n_total += 1
            if len(record.seq) >= min_length:
                good_contigs.append(record)
                n_remaining += 1

        logging.info('Filtered Assembly to ' + str(n_remaining) + ' contigs out of ' + str(n_total))
        filtered_fasta_file = os.path.join(self.shared_folder, 'filtered.fasta')
        SeqIO.write(good_contigs, filtered_fasta_file, 'fasta')


        # Step 4 - Save the new Assembly back to the system
        logging.info('Uploading filtered Assembly data.')
        new_assembly = assemblyUtil.save_assembly_from_fasta({'file': {'path': filtered_fasta_file},
                                                              'workspace_name': workspace_name,
                                                              'assembly_name': fasta_file['assembly_name']
                                                              })


        # Step 5 - Build a Report and return
        reportObj = {
            'objects_created': [{'ref': new_assembly, 'description': 'Filtered contigs'}],
            'text_message': 'Filtered Assembly to ' + str(n_remaining) + ' contigs out of ' + str(n_total)
        }
        report = KBaseReport(self.callback_url)
        report_info = report.create({'report': reportObj, 'workspace_name': params['workspace_name']})


        # STEP 6: contruct the output to send back
        output = {'report_name': report_info['name'],
                  'report_ref': report_info['ref'],
                  'assembly_output': new_assembly,
                  'n_initial_contigs': n_total,
                  'n_contigs_removed': n_total - n_remaining,
                  'n_contigs_remaining': n_remaining
                  }
        logging.info('returning:' + pformat(output))
                
        #END run_omreegalozContigFilter

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_omreegalozContigFilter return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def run_omreegalozContigFilter_max(self, ctx, params):
        """
        New app which filters contigs in an assembly using both a minimum and a maximum contig length
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_omreegalozContigFilter_max
        

        #DEBUG: Print Hello
        print("HELLO AGAIN, WE ARE HERE NOW!")

 
        #DEBUG: Print params
        print(params)      

        if 'assembly_input_ref' not in params:
            raise ValueError('Parameter assembly_input_ref is not set in input arguments')

        assembly_input_ref = params['assembly_input_ref']


        assemblyUtil = AssemblyUtil(self.callback_url)
        fasta_file = assemblyUtil.get_assembly_as_fasta({'ref': assembly_input_ref})
        #print(fasta_file)


        if name not in params:
                raise ValueError('Parameter "' + name + '" is required but missing')
        if not isinstance(params['min_length'], int) or (params['min_length'] < 0):
            raise ValueError('Min length must be a non-negative integer')
        if not isinstance(params['max_length'], int) or (params['max_length'] < 0):
            raise ValueError('Max length must be a non-negative integer')
        if not isinstance(params['assembly_input_ref'], str) or not len(params['assembly_input_ref']):
            raise ValueError('Pass in a valid assembly reference string')
        if (params['max_length'] < params['min_length']):
            raise ValueError('max length must be greater than min length')
        print(params['min_length'], params['max_length'], params['assembly_input_ref'])





        parsed_assembly = SeqIO.parse(fasta_file['path'], 'fasta')
        min_length = params['min_length']
        max_length = params['max_length']

        #Good contigs above min length
        good_contigs = []

        # total contigs regardless of length
        n_total = 0
        # total contigs over the min_length
        n_remaining = 0

        for record in parsed_assembly:
            n_total += 1
            if len(record.seq) >= min_length and len(record.seq) <= max_length:
                good_contigs.append(record)
                n_remaining += 1
        output = {
            'n_total': n_total,
            'n_remaining': n_remaining
        }





        #fasta_file = assembly_util.get_assembly_as_fasta({'ref': params['assembly_ref']})
        #END run_omreegalozContigFilter_max

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_omreegalozContigFilter_max return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
