<%inherit file="/base_panels.mako"/>

## Default title
<%def name="title()">$HEADER_TITLE</%def>

<%def name="javascripts()">
    ${parent.javascripts()}
    ${h.js( "jquery.tipsy" )}
</%def>

## Masthead
<%def name="masthead()">

    ## Tab area, fills entire width
    <div style="position: relative; right: -50%; float: left; text-align: center;">
    
    <table class="tab-group" border="0" cellspacing="0" style="position: fixed; height: 32px; right: 120px;">
    <tr>
    
    <%def name="tab( id, display, href, target='_self', visible=True, extra_class='', menu_options=None )">
        ## Create a tab at the top of the panels. menu_options is a list of 2-elements lists of [name, link]
        ## that are options in the menu.
    
        <%
        cls = "tab"
        if extra_class:
            cls += " " + extra_class
        if self.active_view == id:
            cls += " active"
        style = ""
        if not visible:
            style = "display: none;"
        %>
        <td class="${cls}" style="${style}">
            %if href:
                <a target="${target}" href="${href}">${display}</a>
            %else:
                <a>${display}</a>
            %endif
            %if menu_options:
                <div class="submenu">
                <ul>
                    %for menu_item in menu_options:
                        <li>
                        %if not menu_item:
                            <hr style="color: inherit; background-color: gray"/></li>
                        %else:
                            %if len ( menu_item ) == 1:
                                ${menu_item[0]}
                            %elif len ( menu_item ) == 2:
                                <% name, link = menu_item %>
                                <a href="${link}">${name}</a></li>
                            %else:
                                <% name, link, target = menu_item %>
                                <a target="${target}" href="${link}">${name}</a></li>
                            %endif
                        %endif
                    %endfor
                </ul>
                </div>
            %endif
        </td>
    </%def>
    

    ## Analyze data tab.
    ${tab( "analysis", _("Analyze Data"), h.url_for( controller='/root', action='index' ) )}
    
    ## Workflow tab.
    ${tab( "workflow", _("Workflow"), h.url_for( controller='/workflow', action='index' ) )}
    
    ## 'Shared Items' or Libraries tab.
    <%
        menu_options = [ 
                        [ _('Data Libraries'), h.url_for( controller='/library', action='index') ],
                        None,
                        [ _('Published Histories'), h.url_for( controller='/history', action='list_published' ) ],
                        [ _('Published Workflows'), h.url_for( controller='/workflow', action='list_published' ) ]
                       ]
        if app.config.get_bool( 'enable_tracks', False ):
            menu_options.append( [ _('Published Visualizations'), h.url_for( controller='/visualization', action='list_published' ) ] )        
        if app.config.get_bool( 'enable_pages', False ):
            menu_options.append( [ _('Published Pages'), h.url_for( controller='/page', action='list_published' ) ] )
        tab( "shared", _("Shared Data"), h.url_for( controller='/library', action='index'), menu_options=menu_options )
    %>
    
    ## Lab menu.
    <%
        menu_options = [
                         [ _('Sequencing Requests'), h.url_for( controller='/requests', action='index' ) ],
                         [ _('Find Samples'), h.url_for( controller='/requests', action='find_samples_index' ) ],
                         [ _('Help'), app.config.get( "lims_doc_url", "http://main.g2.bx.psu.edu/u/rkchak/p/sts" ), "galaxy_main" ]
                       ]
        tab( "lab", "Lab", None, menu_options=menu_options, visible=( trans.user and ( trans.user.requests or trans.app.security_agent.get_accessible_request_types( trans, trans.user ) ) ) )
    %>

    ## Visualization menu.
    %if app.config.get_bool( 'enable_tracks', False ):
        <%
            menu_options = [
                             [_('New Visualization'), h.url_for( controller='/tracks', action='index' ) ],
                             [_('Saved Visualizations'), h.url_for( controller='/visualization', action='list' ) ]
                           ]
            tab( "visualization", _("Visualization"), h.url_for( controller='/visualization', action='list'), menu_options=menu_options )
        %>
    %endif

    ## Admin tab.
    ${tab( "admin", "Admin", h.url_for( controller='/admin', action='index' ), extra_class="admin-only", visible=( trans.user and app.config.is_admin_user( trans.user ) ) )}
    
    ## Help tab.
    <%
        menu_options = [
                            [_('HyperBrowser help'), app.config.get( "hyperbrowser_help_url", "http://sites.google.com/site/hyperbrowserhelp/" ), "_blank" ],
                            [_('Support'), app.config.get( "support_url", "http://wiki.g2.bx.psu.edu/Support" ), "_blank" ],
                            [_('Galaxy Wiki'), app.config.get( "wiki_url", "http://wiki.g2.bx.psu.edu/" ), "_blank" ],
                            [_('Video tutorials (screencasts)'), app.config.get( "screencasts_url", "http://galaxycast.org" ), "_blank" ],
                            [_('How to Cite Galaxy'), app.config.get( "citation_url", "http://wiki.g2.bx.psu.edu/Citing%20Galaxy" ), "_blank" ]
                        ]
        tab( "help", _("Help"), None, menu_options=menu_options)
    %>
    
    ## User tabs.
    <%  
        # Menu for user who is not logged in.
        menu_options = [ [ _("Login"), h.url_for( controller='/user', action='login' ), "galaxy_main" ] ]
        if app.config.allow_user_creation:
            menu_options.append( [ _("Register"), h.url_for( controller='/user', action='create', cntrller='user', webapp='galaxy' ), "galaxy_main" ] ) 
        extra_class = "loggedout-only"
        visible = ( trans.user == None )
        tab( "user", _("User"), None, visible=visible, menu_options=menu_options )
        
        # Menu for user who is logged in.
        if trans.user:
            email = trans.user.email
        else:
            email = ""
        menu_options = [ [ '<li>Logged in as <span id="user-email">%s</span></li>' %  email ] ]
        if app.config.use_remote_user:
            if app.config.remote_user_logout_href:
                menu_options.append( [ _('Logout'), app.config.remote_user_logout_href, "_top" ] )
        else:
            menu_options.append( [ _('Preferences'), h.url_for( controller='/user', action='index', cntrller='user', webapp='galaxy' ), "galaxy_main" ] )
            if app.config.get_bool( 'enable_tracks', False ):
                menu_options.append( [ 'Custom Builds', h.url_for( controller='/user', action='dbkeys' ), "galaxy_main" ] )
            if app.config.require_login:
                logout_url = h.url_for( controller='/root', action='index', m_c='user', m_a='logout', webapp='galaxy' )
            else:
                logout_url = h.url_for( controller='/user', action='logout', webapp='galaxy' )
            menu_options.append( [ 'Logout', logout_url, "_top" ] )
            menu_options.append( None )
        menu_options.append( [ _('Saved Histories'), h.url_for( controller='/history', action='list' ), "galaxy_main" ] )
        menu_options.append( [ _('Saved Datasets'), h.url_for( controller='/dataset', action='list' ), "galaxy_main" ] )
        if app.config.get_bool( 'enable_pages', False ):
            menu_options.append( [ _('Saved Pages'), h.url_for( controller='/page', action='list' ), "_top" ] )
        if app.config.enable_api:
            menu_options.append( [ _('API Keys'), h.url_for( controller='/user', action='api_keys', cntrller='user', webapp='galaxy' ), "galaxy_main" ] )
        if app.config.use_remote_user:
            menu_options.append( [ _('Public Name'), h.url_for( controller='/user', action='edit_username', cntrller='user', webapp='galaxy' ), "galaxy_main" ] )
    
        extra_class = "loggedin-only"
        visible = ( trans.user != None )
        tab( "user", "User", None, visible=visible, menu_options=menu_options )
    %>
    
    </tr>
    </table>
    
    </div>
    
    ## Logo, layered over tabs to be clickable
    <div class="title" style="position: absolute; top: 0; left: 0;">
        <a href="${app.config.get( 'logo_url', '/' )}">
        <img border="0" src="${h.url_for('/static/hyperbrowser/images/logo/HB_logo_title_small.png')}" style="width: 391px; vertical-align: top;">
        </a>
        <div style="font-size: 11px; position: absolute; left:409px; top: 10px; width: 200px"><a href='http://main.g2.bx.psu.edu/'>(powered by Galaxy)</a></div>
    </div>

    ## Quota meter
    <%
        bar_style = "quota-meter-bar"
        usage = 0
        percent = 0
        quota = None
        try:
            usage = trans.app.quota_agent.get_usage( trans=trans )
            quota = trans.app.quota_agent.get_quota( trans.user )
            percent = trans.app.quota_agent.get_percent( usage=usage, quota=quota )
            if percent is not None:
                if percent >= 100:
                    bar_style += " quota-meter-bar-error"
                elif percent >= 85:
                    bar_style += " quota-meter-bar-warn"
            else:
                percent = 0
        except AssertionError:
            pass # Probably no history yet
        tooltip = None
        if not trans.user and quota and trans.app.config.allow_user_creation:
            if trans.app.quota_agent.default_registered_quota is None or trans.app.quota_agent.default_unregistered_quota < trans.app.quota_agent.default_registered_quota:
                tooltip = "Your disk quota is %s.  You can increase your quota by registering a Galaxy account." % util.nice_size( quota )
    %>

    <div class="quota-meter-container">
        %if tooltip:
        <div id="quota-meter" class="quota-meter tooltip" title="${tooltip}">
        %else:
        <div id="quota-meter" class="quota-meter">
        %endif
            <div id="quota-meter-bar" class="${bar_style}" style="width: ${percent}px;"></div>
            %if quota is not None:
                <div id="quota-meter-text" class="quota-meter-text">Using ${percent}%</div>
            %else:
                <div id="quota-meter-text" class="quota-meter-text">Using ${util.nice_size( usage )}</div>
            %endif
        </div>
    </div>
    
</%def>
