#!/usr/bin/env python3

import relayserver

muu_socket = 11112
muu_ohjain_releportti = 'B'
muu_on_html = "html/Muu-ohjain_on.htm"
muu_off_html = "html/Muu-ohjain_off.htm"



def main():
    mymuuserver=relayserver.relayserver(lampport=muu_socket,
                                         releportti=muu_ohjain_releportti,
                                         on_html=muu_on_html,
                                         off_html=muu_off_html)


if __name__ == '__main__':
    main()
