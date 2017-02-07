# -*- coding: utf-8

import program_info, io, sys, itertools


class Person():
    '''Represents a person in the phone book'''

    def __init__( self, name, phone = 'n/a', birthday = 'n/a', email = 'n/a' ):
        '''Initializes a person'''
        self.name = name
        self.phone = phone
        self.birthday = birthday
        self.email = email


    def Person_Compile_Line( self ):
        '''this compiles a string to search for it in the phonebook .data file and then delete the line'''

        attributes_compiled_line = ''
        attributes_compiled_line += '{}::{}::{}::{}'.format( self.name, self.phone, self.birthday, self.email )

        return attributes_compiled_line


    """def person_edit( self, *args ):
        '''this edits a person in the phonebook'''
        pass"""


    def Person_Show_Info( self ):
        '''shows info about person in format of a list'''
        info_string = 'Name: {}, phone: {}, birthday: {}, email: {}'.format( self.name, self.phone, self.birthday, self.email )
        return info_string



def UserInput():
    """This asks user for an action (enter one of the options from user_action_tuple) and return his action"""

    user_input_list = [ '-a', '-d', '-e', '-s', 'quit' ]

    while True:
        print( '\nType "-a" - add person, "-s" - search, "-e" - edit person, "-d" - delete persion, "quit" - quit the app' )
        user_input = input( 'Select one of the options above ( -a / -s / -e / -d / quit): ' )

        if user_input in user_input_list:
            break

    return user_input



def SearchUser( search_arg = '' ):
    """This searches for a record in phone book and returns found records in dictionary 'found_person' """


    # ask user for a search request
    if search_arg == 'delete':
        search_for = input( '\nSearch for a record you want to delete.\nType something to search or "-ab" to abort: ' )
    elif search_arg == 'edit':
        search_for = input( '\nSearch for a record you want to update.\nType something to search or "-ab" to abort: ' )
    else:
        search_for = input( '\nEnter search phrase or "-ab" to abort: ' )

    # stopping if 'abort'
    if search_for == '-ab':
        found_person = dict()
        return found_person

    # looking for search phrase in file lines and append whole line to the matching list
    with io.open( 'phonebook.data', 'r' ) as phonebook_f:

        matching = []
        for file_line in phonebook_f:
            if search_for in file_line:
                matching.append( file_line.rstrip() )


    # showing the lines from phonebook.data file that contain the search phrase, else say 'nothing found'
    if matching == []:
        print( 'Nothing found' )
        found_person = dict()
        return found_person

    else:
        print( '\nSearch complete. Found:\n' )

        # forming a dictionary to generate object Person
        found_person = dict()
        i = 1

        for element in matching:

            element = element.split( '::' )

            # zipping list of keys into list of read user data
            keyslist = ['name', 'phone', 'bd', 'mail']
            found_keys_values = dict( itertools.zip_longest( keyslist, element ) )

            # generate Person object and put it into a dictionary
            # test!
            found_person[i] = Person( found_keys_values['name'],
                                      found_keys_values['phone'],
                                      found_keys_values['bd'],
                                      found_keys_values['mail'] )
            i += 1

        # print out found persons
        for k, v in found_person.items():
            print ( '>>>  {}. {}'.format( k, v.Person_Show_Info() ) )

        return found_person





#===============================================================================
# Execution
#===============================================================================
if __name__ == "__main__":

    # program says Hi to user
    print( program_info.hello_text.format( program_info.version ) )


    # ask user for an action
    user_input_choise = UserInput()


    # until user types 'quit' we do the job
    while user_input_choise != 'quit':

        #===========================================================================
        # ADDING a record to the book
        #===========================================================================
        if user_input_choise == '-a':

            # entering a name
            while True:
                new_name = input( "Enter a name, it should be more than 2 chars: " )

                if new_name != '' and len( new_name ) > 2:
                    print ( new_name )
                    break

            # entering phone
            new_phone = input( "Enter phone number (optional): " )

            # entering birthday
            new_birthday = input( "Enter birthday (optional): " )

            # entering email
            new_email = input( "Enter email (optional): " )

            # assembling a string for putting it into the file
            new_line = new_name + '::' + new_phone + '::' + new_birthday + '::' + new_email + '\n'

            # creating a new record in file
            with io.open( "phonebook.data", "a" ) as phonebook_f:
                phonebook_f.write( new_line )
                print( '\nThe person "{}" has been added to the phone book successfully!'.format( new_name ) )

            # asking user to make his choise again
            user_input_choise = UserInput()



        #===========================================================================
        # SEARCH for a record in the book
        #===========================================================================
        elif user_input_choise == '-s':

            # searching for a record using a string from user
            SearchUser()

            # asking user to make his choise again
            user_input_choise = UserInput()



        #===========================================================================
        # DELETE a record in the book
        #===========================================================================
        elif user_input_choise == '-d':
            print( "\nWARNING: You are in DELETING mode!" )

            # ask user for a search request and returning
            to_delete_list = SearchUser( 'delete' )


            # if search found something
            if bool( to_delete_list ):

                # forming a list of candidates for deletion
                records_found_to_delete = []
                records_found_to_delete_indices = ''

                for k in to_delete_list:
                    records_found_to_delete.append( str( k ) )

                records_found_to_delete_indices_to_print = ['[' + str( i ) + ']' for i in records_found_to_delete]

                # ask user what to delete
                yes_no = ['y', 'n', '-ab']
                yes_no_answer = ''

                if len( records_found_to_delete ) > 1:
                    print( '\nWhich record you want to delete: {}?'.format( ', '.join( records_found_to_delete_indices_to_print ) ) )

                    # user should type correct number from 'records_found_to_delete' list
                    while True:
                        to_delete_id = input( 'Type a number of the record above to delete it, or "-ab" to abort: ' )

                        # aborting if 'abort'
                        if to_delete_id == '-ab':
                            user_input_choise = ''
                            yes_no_answer = 'n'
                            break

                        elif to_delete_id not in records_found_to_delete:
                            pass

                        else:
                            break

                    # asking once again about deletion is a good thing to do
                    if yes_no_answer == '':
                        yes_no_answer = input( '\nAre you sure? (y/n) ' )

                else:
                    to_delete_id = '1'
                    yes_no_answer = input( '\nAre you sure you want to delete found line? (y/n) ' )


                # getting user's confirmation
                while yes_no_answer not in yes_no:
                    yes_no_answer = input( '\nYou must type "y" or "n" ' )

                else:
                    if yes_no_answer == 'n':

                        yes_no_answer = ''

                        # asking user to make his choise again
                        user_input_choise = UserInput()

                    else:
                        yes_no_answer = ''
                        # deleting record from phonebook
                        print( '\nDeleting line #{}...'.format( to_delete_id ) )

                        # reading lines from .data file
                        with open( 'phonebook.data', 'r' ) as phonebook_f:
                            lines = phonebook_f.readlines()

                        # writing lines back to file, except removed one
                        removed_line = to_delete_list[ int( to_delete_id ) ].Person_Compile_Line()
                        with open( 'phonebook.data', 'w' ) as phonebook_f:
                            for line in lines:
                                if  line.rstrip() != removed_line:
                                    phonebook_f.write( line )

                        # showing message to user
                        print( 'The line has been deleted successfully.' )

                        # asking user to make his choise again
                        user_input_choise = UserInput()


            # if search for deletion didn't find anything, ask user for action again
            else:
                # asking user to make his choise again
                user_input_choise = UserInput()


        #===========================================================================
        # Editing a record
        #===========================================================================
        elif user_input_choise == '-e':

            # ask user to search the line to edit
            to_edit_list = SearchUser( 'edit' )


            # if search found something
            if bool( to_edit_list ):

                # forming a list of candidates for deletion
                records_found_to_edit = []

                for k in to_edit_list:
                    records_found_to_edit.append( str( k ) )

                records_found_to_edit_indices_to_print = ['[' + str( i ) + ']' for i in records_found_to_edit]

                # ask user what to delete
                yes_no = ['y', 'n']
                yes_no_answer = ''

                if len( records_found_to_edit ) > 1:
                    print( '\nWhich record you want to edit: {}?'.format( ', '.join( records_found_to_edit_indices_to_print ) ) )

                    # user should type correct number from 'records_found_to_edit' list
                    while True:
                        to_delete_id = input( 'Type a number of the record above to edit it, or "-ab" to abort: ' )

                        # aborting if 'abort'
                        if to_delete_id == '-ab':
                            user_input_choise = ''
                            yes_no_answer = 'n'
                            break

                        elif to_delete_id not in records_found_to_edit:
                            pass

                        else:
                            break

                    # asking once again about deletion is a good thing to do
                    if yes_no_answer == '':
                        yes_no_answer = input( '\nAre you sure? (y/n) ' )

                else:
                    to_delete_id = '1'
                    yes_no_answer = input( '\nAre you sure you want to edit found line? (y/n) ' )


                # getting user's confirmation
                while yes_no_answer not in yes_no:
                    yes_no_answer = input( '\nYou must type "y" or "n" ' )

                else:
                    if yes_no_answer == 'n':

                        # asking user to make his choise again
                        user_input_choise = UserInput()

                    else:

                        # deleting record from phonebook
                        print( '\nEditing line #{}...'.format( to_delete_id ) )

                        # reading lines from .data file
                        with open( 'phonebook.data', 'r' ) as phonebook_f:
                            lines = phonebook_f.readlines()


                        # writing lines back to file, except the one that will be edited
                        removed_line = to_edit_list[ int( to_delete_id ) ].Person_Compile_Line()
                        person_attributes_to_edit = removed_line.split( '::' )

                        edit_person = Person( person_attributes_to_edit[0],
                                              person_attributes_to_edit[1],
                                              person_attributes_to_edit[2],
                                              person_attributes_to_edit[3] )

                        for k, v in edit_person.__dict__.items():
                            new_v = input( 'Edit [{}] value or hit Enter to preserve current (current is {}): '.format( k, v ) )
                            v = new_v or v
                            setattr( edit_person, k, v )

                        print( 'Updated info is: ', edit_person.Person_Show_Info() )


                        person_attributes_to_write = edit_person.Person_Compile_Line()

                        # writing lines back to file, except the one that was edited...
                        with open( 'phonebook.data', 'w' ) as phonebook_f:
                            for line in lines:
                                if  line.rstrip() != removed_line:
                                    phonebook_f.write( line )

                            # ... and append edited line to the file
                            phonebook_f.write( person_attributes_to_write )


                        # showing message to user
                        print( 'The line has been edited successfully!' )

                        # asking user to make his choise again
                        user_input_choise = UserInput()


            # if search for deletion didn't find anything, ask user for action again
            else:
                # asking user to make his choise again
                user_input_choise = UserInput()


    else:
        print( '\nThanks for using Phonebook!' )
        sys.exit( 0 )





# Copyright (c) 2016, Konstantin Chernukhin, All rights reserved.
# Created as a part of learning and practicing process.
#
# Author's url: http://octogear.com
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# IABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
