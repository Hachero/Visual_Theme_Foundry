# Icon Reference: Taxonomy and File Mapping

Generated: 2026-04-02 20:24:00

This document defines core and specialized icon groups, then maps each generic name to matching filenames in both reference source folders:

- \_references/icons-original/
- \_references/icons-original/ionicons-svg/

Normalized output note: normalized icons are now flattened into:

- icons/normalized/light/
- icons/normalized/normal/
- icons/normalized/medium/

Organization note: the original source SVGs were moved out of the runtime-facing icons folder and now live under \_references/icons-original/. The detailed group listings below may still use the legacy `icons/` and `icons/ionicons-svg/` labels as shorthand for those reference sources.

## 1) Core Web-App Icon Groups

### 1.1 Main-Primary (18)

Main-primary set: [Home, Search, Menu, Close, Add, Edit, Delete/Remove, Save, Settings, User/Profile, People/Team, Notifications/Alerts, Message/Chat, Calendar/Schedule, File/Document, Folder, Upload/Download, Share].

Coverage target note: each group should have at least 4 options in the normalized catalog.

### 1.1b Main-Primary Role and Palette Mapping

Design intent: this mapping is a predictable default contract, not an absolute rule. Use semantic colors only when the icon is communicating semantic state.

| Main-Primary Group   | Typical Role                      | Default Token              | Active/Selected Token                 | Notes                                                                                    |
| -------------------- | --------------------------------- | -------------------------- | ------------------------------------- | ---------------------------------------------------------------------------------------- |
| Home                 | Navigation destination            | on-surface-variant         | primary                               | If using selected containers/chips, use on-secondary-container on the selected container |
| Search               | Utility action / input affordance | on-surface-variant         | primary when focused/open             | In text fields, search can stay neutral until focus/active state                         |
| Menu                 | UI chrome toggle                  | on-surface                 | primary when drawer/panel is open     | Keep neutral in top app bars by default                                                  |
| Close                | Dismiss/cancel control            | on-surface                 | on-surface                            | Use error only when close implies destructive removal                                    |
| Add                  | Constructive action               | primary for emphasized CTA | on-primary in filled primary button   | Use on-surface for low-emphasis add actions                                              |
| Edit                 | Secondary utility action          | on-surface                 | primary when current tool/mode        | Avoid semantic state colors for generic edit                                             |
| Delete/Remove        | Destructive action                | error                      | on-error in filled destructive button | Semantic exception: destructive intent should be explicit                                |
| Save                 | Commit/persist action             | primary when emphasized    | on-primary in filled primary button   | Keep neutral if save is available but not emphasized                                     |
| Settings             | Navigation to preferences         | on-surface-variant         | primary when active route             | Usually a nav/utility role, not semantic state                                           |
| User/Profile         | Identity/account destination      | on-surface-variant         | primary when selected                 | Avatar/image can override glyph color choices                                            |
| People/Team          | Entity/object category            | on-surface                 | primary when selected/filter active   | Treat as object icon by default                                                          |
| Notifications/Alerts | Status entry point                | on-surface-variant         | primary when active route             | Badge carries semantic color (error/warning), not the base icon by default               |
| Message/Chat         | Communication destination/action  | on-surface-variant         | primary when selected                 | Unread indicators should be badges/state markers                                         |
| Calendar/Schedule    | Object/action hybrid              | on-surface                 | primary when selected                 | Keep neutral unless actively selected                                                    |
| File/Document        | Object type                       | on-surface                 | primary when selected                 | Category icons remain neutral unless taxonomy colors are formally defined                |
| Folder               | Object/container type             | on-surface                 | primary when selected                 | Same guidance as File/Document                                                           |
| Upload/Download      | Directional action                | on-surface                 | primary when active/invoked           | Progress should use separate indicators, not full icon recolor                           |
| Share                | Outbound action                   | on-surface                 | primary for emphasized share CTA      | Keep neutral in menus and secondary action rows                                          |

Quick pairing rule:

- Use role color + matching on-role foreground when icon sits on a filled container (for example: primary + on-primary, secondary-container + on-secondary-container, error + on-error).
- Use on-surface or on-surface-variant as the app-wide default icon color baseline.
- Promote to primary only for active/selected/current states or explicitly emphasized actions.

### 1.1a Coverage Audit (Normalized Light)

Audit source: icons/normalized/light/ (flattened; 1023 icons)

Under-represented groups (<4 matches):

- Database (patterns: database) -> 1 match

#### Home

- Generic patterns: home
- icons/: home-outline.svg
- icons/ionicons-svg/: home-01.svg, home-02.svg, home-outline-01.svg

#### Search

- Generic patterns: search
- icons/: search-outline.svg
- icons/ionicons-svg/: search-01.svg, search-02.svg, search-outline-01.svg

#### Menu

- Generic patterns: menu
- icons/: menu.svg
- icons/ionicons-svg/: menu-01.svg, menu-02.svg, menu-outline-01.svg

#### Close

- Generic patterns: close
- icons/: close-circle-outline.svg, close.svg
- icons/ionicons-svg/: close-01.svg, close-02.svg, close-circle-01.svg, close-circle-02.svg, close-circle-outline-01.svg, closed-captioning-01.svg, closed-captioning-02.svg, closed-captioning-outline-01.svg

#### Add

- Generic patterns: add
- icons/: add-circle-outline.svg, add.svg, document-add.svg, person-add-outline.svg, report-add.svg
- icons/ionicons-svg/: add-01.svg, add-02.svg, add-circle-01.svg, add-circle-02.svg, add-circle-outline-01.svg, person-add-01.svg, person-add-02.svg, person-add-outline-01.svg

#### Edit

- Generic patterns: edit, create, pencil
- icons/: create-outline.svg, message-edit-square.svg, message-edit.svg
- icons/ionicons-svg/: create-01.svg, create-02.svg, create-outline-01.svg

#### Delete/Remove

- Generic patterns: delete, remove, trash
- icons/: remove-circle-outline.svg, trash-outline.svg
- icons/ionicons-svg/: remove-01.svg, remove-02.svg, remove-circle-01.svg, remove-circle-02.svg, remove-circle-outline-01.svg, trash-01.svg, trash-02.svg, trash-outline-01.svg

#### Save

- Generic patterns: save, disk, disc, floppy
- icons/: device-floppy-save.svg, ic_fluent_save_24_filled.svg, ic_fluent_save_24_regular.svg, save-outline-01.svg, save-outline.svg, save.svg
- icons/ionicons-svg/: disc-01.svg, disc-02.svg, disc-outline-01.svg

#### Settings

- Generic patterns: settings, options, cog
- icons/: options-outline.svg, settings-outline.svg
- icons/ionicons-svg/: cog-01.svg, cog-02.svg, cog-outline-01.svg, options-01.svg, options-02.svg, options-outline-01.svg, settings-01.svg, settings-02.svg, settings-outline-01.svg

#### User/Profile

- Generic patterns: person, user, profile, contact
- icons/: contact-outline.svg, contacts-outline.svg, person-add-outline.svg, person-outline.svg
- icons/ionicons-svg/: contact-01.svg, contact-02.svg, contact-outline-01.svg, contacts-01.svg, contacts-02.svg, contacts-outline-01.svg, person-01.svg, person-02.svg, person-add-01.svg, person-add-02.svg, person-add-outline-01.svg, person-outline-01.svg

#### People/Team

- Generic patterns: people, contacts, group, team
- icons/: contacts-outline.svg, people-outline.svg
- icons/ionicons-svg/: contacts-01.svg, contacts-02.svg, contacts-outline-01.svg, people-01.svg, people-02.svg, people-outline-01.svg, steam-01.svg

#### Notifications/Alerts

- Generic patterns: alert, notification, bell, warning
- icons/: alert-outline.svg, oil-derrick-warning.svg
- icons/ionicons-svg/: alert-01.svg, alert-02.svg, alert-outline-01.svg, notifications-01.svg, notifications-02.svg, notifications-off-01.svg, notifications-off-02.svg, notifications-off-outline-01.svg, notifications-outline-01.svg, notifications-outline-02.svg, warning-01.svg, warning-02.svg, warning-outline-01.svg

#### Message/Chat

- Generic patterns: message, messages, chat, mail
- icons/: chatboxes-outline.svg, chatbubbles-outline.svg, message-edit-square.svg, message-edit.svg, messages.svg
- icons/ionicons-svg/: chatboxes-01.svg, chatboxes-02.svg, chatboxes-outline-01.svg, chatbubbles-01.svg, chatbubbles-02.svg, chatbubbles-outline-01.svg, mail-01.svg, mail-02.svg, mail-open-01.svg, mail-open-02.svg, mail-open-outline-01.svg, mail-outline-01.svg, snapchat-01.svg

#### Calendar/Schedule

- Generic patterns: calendar, schedule, time, clock
- icons/: calendar-outline.svg, schedule.svg
- icons/ionicons-svg/: calendar-01.svg, calendar-02.svg, calendar-outline-01.svg, clock-01.svg, clock-02.svg, clock-outline-01.svg, time-01.svg, time-02.svg, time-outline-01.svg, timer-01.svg, timer-02.svg, timer-outline-01.svg

#### File/Document

- Generic patterns: file, document, paper, clipboard, invoice, report
- icons/: clipboard-outline.svg, document-add.svg, document-outline.svg, invoice.svg, paper-outline.svg, report-add.svg, reports-flagged-red.svg, reports-flagged-red2.svg, reports-flagged.svg, reports-misc-large.svg, reports-misc.svg, reports-work.svg, reports.original.svg, reports.svg, shift-reports.svg
- icons/ionicons-svg/: clipboard-01.svg, clipboard-02.svg, clipboard-outline-01.svg, document-01.svg, document-02.svg, document-outline-01.svg, paper-01.svg, paper-02.svg, paper-outline-01.svg, paper-plane-01.svg, paper-plane-02.svg, paper-plane-outline-01.svg

#### Folder

- Generic patterns: folder, filing, archive
- icons/: archive-outline.svg, filing-outline.svg, folder-open-outline.svg, folder-outline.svg, folder-verified-outline.svg
- icons/ionicons-svg/: archive-01.svg, archive-02.svg, archive-outline-01.svg, filing-01.svg, filing-02.svg, filing-outline-01.svg, folder-01.svg, folder-02.svg, folder-open-01.svg, folder-open-02.svg, folder-open-outline-01.svg, folder-outline-01.svg

#### Upload/Download

- Generic patterns: upload, download, log-in, log-out, import, export
- icons/: download-outline.svg, log-in.svg, log-out.svg
- icons/ionicons-svg/: cloud-download-01.svg, cloud-download-02.svg, cloud-download-outline-01.svg, cloud-upload-01.svg, cloud-upload-02.svg, cloud-upload-outline-01.svg, code-download-01.svg, code-download-02.svg, download-01.svg, download-02.svg, download-outline-01.svg, log-in-01.svg, log-in-02.svg, log-out-01.svg, log-out-02.svg

#### Share

- Generic patterns: share, send
- icons/: share-outline.svg
- icons/ionicons-svg/: send-01.svg, send-02.svg, send-outline-01.svg, share-01.svg, share-02.svg, share-alt-01.svg, share-alt-02.svg, share-alt-outline-01.svg, share-outline-01.svg

### 1.2 Sub-Main Groups by Usage

### 1.2a Sub-Main Role and Palette Mapping (Predictable Defaults)

Design intent: these mappings define default behavior by role family. They are strong defaults, not hard constraints.

#### Navigation and Wayfinding: Palette Mapping

| Sub-Group    | Typical Role               | Default Token      | Active/Selected Token                        | Notes                                                                       |
| ------------ | -------------------------- | ------------------ | -------------------------------------------- | --------------------------------------------------------------------------- |
| Back/Forward | Navigation control         | on-surface         | primary when current route step is active    | Keep neutral for generic back buttons                                       |
| Up/Down      | Directional affordance     | on-surface-variant | primary when expanded/current sort direction | Good candidate for subtle state toggles                                     |
| Location/Map | Destination/context        | on-surface-variant | primary when selected/current location       | If map marker is semantic (incident), use semantic color only in that state |
| Open/Exit    | Session/context transition | on-surface         | primary when emphasized                      | Use error only when action is destructive/irreversible                      |

#### Content and File Operations: Palette Mapping

| Sub-Group | Typical Role          | Default Token      | Active/Selected Token                    | Notes                                                                      |
| --------- | --------------------- | ------------------ | ---------------------------------------- | -------------------------------------------------------------------------- |
| Document  | Object type           | on-surface         | primary when selected                    | Keep object icons neutral in lists/tables                                  |
| Folder    | Object/container type | on-surface         | primary when selected/open target        | Same behavior as document icons                                            |
| Copy      | Utility action        | on-surface         | primary when action is emphasized        | Confirmation state should be separate (toast/check), not permanent recolor |
| Print     | Utility action        | on-surface         | primary when emphasized                  | Often appears in overflow menus, so neutral is preferred                   |
| List/Grid | View mode toggle      | on-surface-variant | primary for currently selected view mode | Ideal for binary/segmented toggle cues                                     |

#### Communication: Palette Mapping

| Sub-Group  | Typical Role       | Default Token      | Active/Selected Token               | Notes                                                       |
| ---------- | ------------------ | ------------------ | ----------------------------------- | ----------------------------------------------------------- |
| Chat       | Destination/action | on-surface-variant | primary when selected/open thread   | Unread should be badge/state, not base icon recolor         |
| Mail       | Destination/action | on-surface-variant | primary when selected               | Unread and priority belong to badges/metadata               |
| Call       | Immediate action   | on-surface         | primary when active/in-call control | Escalation states can use semantic colors where appropriate |
| Share/Send | Outbound action    | on-surface         | primary when emphasized CTA         | Keep neutral in contextual action menus                     |

#### Status and Feedback: Palette Mapping

| Sub-Group     | Typical Role             | Default Token                                     | Active/Selected Token                   | Notes                                                                      |
| ------------- | ------------------------ | ------------------------------------------------- | --------------------------------------- | -------------------------------------------------------------------------- |
| Info/Help     | Neutral/supportive state | on-surface-variant                                | tertiary for mild emphasis              | Avoid warning/error unless state is actually abnormal                      |
| Success/Check | Positive semantic state  | success (or primary if success token unavailable) | on-success on filled success container  | Semantic colorized by default is acceptable here                           |
| Warning/Error | Negative semantic state  | warning or error                                  | on-warning/on-error on filled container | Semantic exception by design                                               |
| Refresh/Sync  | Process/status action    | on-surface                                        | primary when running/active             | Long-running sync should use progress indicators in addition to icon color |
| Visibility    | State toggle (show/hide) | on-surface                                        | primary when explicitly toggled on      | Use neutral for passive visibility affordances                             |

#### Data, Analytics, and Reporting: Palette Mapping

| Sub-Group     | Typical Role                    | Default Token      | Active/Selected Token                | Notes                                                                      |
| ------------- | ------------------------------- | ------------------ | ------------------------------------ | -------------------------------------------------------------------------- |
| Charts/Stats  | Data object/insight category    | on-surface         | primary when selected/current metric | Keep neutral in dense dashboards to reduce visual noise                    |
| Reports       | Data artifact                   | on-surface         | primary when selected                | Semantic colors should represent report status, not the report icon itself |
| Database      | Technical object/infrastructure | on-surface         | primary when selected/active target  | Infra alarms and faults can override with warning/error states             |
| Search/Filter | Utility action/state            | on-surface-variant | primary when filter/search is active | Active filter count should be shown separately where possible              |

Cross-group pairing rules:

- Default icon baseline is on-surface or on-surface-variant.
- Use primary for active, selected, focused, or intentionally emphasized actions.
- Use on-\* foreground tokens when an icon is placed on a filled role/container background.
- Reserve semantic palettes (error, warning, success, info) for true state signaling.

#### Navigation & Wayfinding

- Back/Forward
  - Generic patterns: arrow-back, arrow-forward, back, forward, return-left, return-right
  - icons/: arrow-back.svg, arrow-forward.svg
  - icons/ionicons-svg/: arrow-back-01.svg, arrow-back-02.svg, arrow-forward-01.svg, arrow-forward-02.svg, arrow-round-back-01.svg, arrow-round-back-02.svg, arrow-round-forward-01.svg, arrow-round-forward-02.svg, backspace-01.svg, backspace-02.svg, backspace-outline-01.svg, fastforward-01.svg, fastforward-02.svg, fastforward-outline-01.svg, return-left-01.svg, return-left-02.svg, return-right-01.svg, return-right-02.svg, skip-backward-01.svg, skip-backward-02.svg, skip-backward-outline-01.svg, skip-forward-01.svg, skip-forward-02.svg, skip-forward-outline-01.svg
- Up/Down
  - Generic patterns: arrow-up, arrow-down, chevron, dropdown, dropup, up, down
  - icons/: arrow-down.svg, arrow-up.svg, download-outline.svg
  - icons/ionicons-svg/: arrow-down-01.svg, arrow-down-02.svg, arrow-dropdown-01.svg, arrow-dropdown-02.svg, arrow-dropdown-circle-01.svg, arrow-dropdown-circle-02.svg, arrow-dropup-01.svg, arrow-dropup-02.svg, arrow-dropup-circle-01.svg, arrow-dropup-circle-02.svg, arrow-round-down-01.svg, arrow-round-down-02.svg, arrow-round-up-01.svg, arrow-round-up-02.svg, arrow-up-01.svg, arrow-up-02.svg, cloud-download-01.svg, cloud-download-02.svg, cloud-download-outline-01.svg, cloud-upload-01.svg, cloud-upload-02.svg, cloud-upload-outline-01.svg, code-download-01.svg, code-download-02.svg, download-01.svg, download-02.svg, download-outline-01.svg, markdown-01.svg, thumbs-down-01.svg, thumbs-down-02.svg, thumbs-down-outline-01.svg, thumbs-up-01.svg, thumbs-up-02.svg, thumbs-up-outline-01.svg, trending-down-01.svg, trending-down-02.svg, trending-up-01.svg, trending-up-02.svg, volume-down-01.svg, volume-down-02.svg, volume-up-01.svg, volume-up-02.svg
- Location/Map
  - Generic patterns: location, locate, map, navigate, compass, gps, geolocation, pin
  - icons/: compass-outline.svg, geolocation-earth.svg, geolocation.svg, gps-icon.svg, gps.svg, locate-outline.svg, location-history-map-large.svg, location-history-map.svg, location-history-pin.svg, location-outline.svg, location-trail.svg, map-outline.svg, navigate-outline.svg, oil-location.svg
  - icons/ionicons-svg/: compass-01.svg, compass-02.svg, compass-outline-01.svg, locate-01.svg, locate-02.svg, locate-outline-01.svg, map-01.svg, map-02.svg, map-outline-01.svg, navigate-01.svg, navigate-02.svg, navigate-outline-01.svg, pin-01.svg, pin-02.svg, pin-outline-01.svg, pint-01.svg, pint-02.svg, pint-outline-01.svg, pinterest-01.svg
- Open/Exit
  - Generic patterns: open, exit
  - icons/: exit-outline.svg, folder-open-outline.svg, open-outline.svg
  - icons/ionicons-svg/: exit-01.svg, exit-02.svg, exit-outline-01.svg, folder-open-01.svg, folder-open-02.svg, folder-open-outline-01.svg, mail-open-01.svg, mail-open-02.svg, mail-open-outline-01.svg, open-01.svg, open-02.svg, open-outline-01.svg

#### Content & File Operations

- Document
  - Generic patterns: document, paper, clipboard
  - icons/: clipboard-outline.svg, document-add.svg, document-outline.svg, paper-outline.svg
  - icons/ionicons-svg/: clipboard-01.svg, clipboard-02.svg, clipboard-outline-01.svg, document-01.svg, document-02.svg, document-outline-01.svg, paper-01.svg, paper-02.svg, paper-outline-01.svg, paper-plane-01.svg, paper-plane-02.svg, paper-plane-outline-01.svg
- Folder
  - Generic patterns: folder, archive, filing
  - icons/: archive-outline.svg, filing-outline.svg, folder-open-outline.svg, folder-outline.svg, folder-verified-outline.svg
  - icons/ionicons-svg/: archive-01.svg, archive-02.svg, archive-outline-01.svg, filing-01.svg, filing-02.svg, filing-outline-01.svg, folder-01.svg, folder-02.svg, folder-open-01.svg, folder-open-02.svg, folder-open-outline-01.svg, folder-outline-01.svg
- Copy
  - Generic patterns: copy
  - icons/: copy-form.svg, copy-list.svg, copy-outline.svg, copy-table.svg
  - icons/ionicons-svg/: copy-01.svg, copy-02.svg, copy-outline-01.svg
- Print
  - Generic patterns: print
  - icons/: print-outline.svg
  - icons/ionicons-svg/: finger-print-01.svg, finger-print-02.svg, print-01.svg, print-02.svg, print-outline-01.svg
- List/Grid
  - Generic patterns: list, grid, table, split, reorder
  - icons/: copy-list.svg, copy-table.svg, list-box-outline.svg, reorder.svg, split-vertical.svg, split.svg, tablet-landscape.svg, tablet-portrait.svg
  - icons/ionicons-svg/: grid-01.svg, grid-02.svg, grid-outline-01.svg, list-01.svg, list-02.svg, list-box-01.svg, list-box-02.svg, list-box-outline-01.svg, reorder-01.svg, reorder-02.svg, tablet-landscape-01.svg, tablet-landscape-02.svg, tablet-portrait-01.svg, tablet-portrait-02.svg

#### Communication

- Chat
  - Generic patterns: chat, message, messages
  - icons/: chatboxes-outline.svg, chatbubbles-outline.svg, message-edit-square.svg, message-edit.svg, messages.svg
  - icons/ionicons-svg/: chatboxes-01.svg, chatboxes-02.svg, chatboxes-outline-01.svg, chatbubbles-01.svg, chatbubbles-02.svg, chatbubbles-outline-01.svg, snapchat-01.svg
- Mail
  - Generic patterns: mail
  - icons/: None
  - icons/ionicons-svg/: mail-01.svg, mail-02.svg, mail-open-01.svg, mail-open-02.svg, mail-open-outline-01.svg, mail-outline-01.svg
- Call
  - Generic patterns: call, phone
  - icons/: call-outline.svg, phone-in-hand-2.svg, phone-in-hand.svg, phone-landscape.svg, phone-portrait.svg
  - icons/ionicons-svg/: call-01.svg, call-02.svg, call-outline-01.svg, megaphone-01.svg, megaphone-02.svg, megaphone-outline-01.svg, microphone-01.svg, microphone-02.svg, microphone-outline-01.svg, phone-landscape-01.svg, phone-landscape-02.svg, phone-portrait-01.svg, phone-portrait-02.svg
- Share/Send
  - Generic patterns: share, send
  - icons/: share-outline.svg
  - icons/ionicons-svg/: send-01.svg, send-02.svg, send-outline-01.svg, share-01.svg, share-02.svg, share-alt-01.svg, share-alt-02.svg, share-alt-outline-01.svg, share-outline-01.svg

#### Status & Feedback

- Info/Help
  - Generic patterns: information, info, help
  - icons/: help-circle-outline.svg, information-circle-outline.svg
  - icons/ionicons-svg/: help-01.svg, help-02.svg, help-buoy-01.svg, help-buoy-02.svg, help-buoy-outline-01.svg, help-circle-01.svg, help-circle-02.svg, help-circle-outline-01.svg, information-01.svg, information-02.svg, information-circle-01.svg, information-circle-02.svg, information-circle-outline-01.svg
- Success/Check
  - Generic patterns: check, verified, done
  - icons/: box-check-no.svg, box-check-yes.svg, flag-checkered.svg, folder-verified-outline.svg
  - icons/ionicons-svg/: checkbox-01.svg, checkbox-02.svg, checkbox-outline-01.svg, checkbox-outline-02.svg, checkmark-01.svg, checkmark-02.svg, checkmark-circle-01.svg, checkmark-circle-02.svg, checkmark-circle-outline-01.svg, checkmark-circle-outline-02.svg, cloud-done-01.svg, cloud-done-02.svg, cloud-done-outline-01.svg, done-all-01.svg, done-all-02.svg
- Warning/Error
  - Generic patterns: warning, problem, error, alert
  - icons/: alert-outline.svg, employee-problem.svg, oil-derrick-problem.svg, oil-derrick-warning.svg, problems.svg
  - icons/ionicons-svg/: alert-01.svg, alert-02.svg, alert-outline-01.svg, warning-01.svg, warning-02.svg, warning-outline-01.svg
- Refresh/Sync
  - Generic patterns: refresh, sync, repeat, reset
  - icons/: database-refresh.svg, refresh-circle-outline.svg, refresh-form.svg, refresh.svg, repeat.svg, reset-form.svg, reset.svg, sync.svg
  - icons/ionicons-svg/: refresh-01.svg, refresh-02.svg, refresh-circle-01.svg, refresh-circle-02.svg, refresh-circle-outline-01.svg, repeat-01.svg, repeat-02.svg, sync-01.svg, sync-02.svg
- Visibility
  - Generic patterns: eye, show, hide
  - icons/: eye-off-outline.svg, eye-outline.svg
  - icons/ionicons-svg/: eye-01.svg, eye-02.svg, eye-off-01.svg, eye-off-02.svg, eye-off-outline-01.svg, eye-outline-01.svg

#### Data, Analytics & Reporting

- Charts/Stats
  - Generic patterns: analytics, stats, pie, pulse, chart
  - icons/: analytics-outline.svg, analytics.svg, pie-outline.svg, pulse-outline.svg, pulse.svg, stats-outline.svg
  - icons/ionicons-svg/: analytics-01.svg, analytics-02.svg, analytics-outline-01.svg, pie-01.svg, pie-02.svg, pie-outline-01.svg, pulse-01.svg, pulse-02.svg, pulse-outline-01.svg, stats-01.svg, stats-02.svg, stats-outline-01.svg
- Reports
  - Generic patterns: report, reports
  - icons/: report-add.svg, reports-flagged-red.svg, reports-flagged-red2.svg, reports-flagged.svg, reports-misc-large.svg, reports-misc.svg, reports-work.svg, reports.original.svg, reports.svg, shift-reports.svg
  - icons/ionicons-svg/: None
- Database
  - Generic patterns: database
  - icons/: database-refresh.svg
  - icons/ionicons-svg/: None
- Search/Filter
  - Generic patterns: search, filter, funnel
  - icons/: search-outline.svg
  - icons/ionicons-svg/: color-filter-01.svg, color-filter-02.svg, color-filter-outline-01.svg, funnel-01.svg, funnel-02.svg, funnel-outline-01.svg, search-01.svg, search-02.svg, search-outline-01.svg

#### Device & Platform

- Desktop/Mobile/Tablet
  - Generic patterns: desktop, laptop, phone, tablet, mobile
  - icons/: phone-in-hand-2.svg, phone-in-hand.svg, phone-landscape.svg, phone-portrait.svg, tablet-landscape.svg, tablet-portrait.svg
  - icons/ionicons-svg/: desktop-01.svg, desktop-02.svg, desktop-outline-01.svg, laptop-01.svg, laptop-02.svg, megaphone-01.svg, megaphone-02.svg, megaphone-outline-01.svg, microphone-01.svg, microphone-02.svg, microphone-outline-01.svg, phone-landscape-01.svg, phone-landscape-02.svg, phone-portrait-01.svg, phone-portrait-02.svg, tablet-landscape-01.svg, tablet-landscape-02.svg, tablet-portrait-01.svg, tablet-portrait-02.svg
- Connectivity
  - Generic patterns: wifi, bluetooth, cloud
  - icons/: None
  - icons/ionicons-svg/: bluetooth-01.svg, bluetooth-02.svg, cloud-01.svg, cloud-02.svg, cloud-circle-01.svg, cloud-circle-02.svg, cloud-circle-outline-01.svg, cloud-done-01.svg, cloud-done-02.svg, cloud-done-outline-01.svg, cloud-download-01.svg, cloud-download-02.svg, cloud-download-outline-01.svg, cloud-outline-01.svg, cloud-outline-02.svg, cloud-upload-01.svg, cloud-upload-02.svg, cloud-upload-outline-01.svg, cloudy-01.svg, cloudy-02.svg, cloudy-night-01.svg, cloudy-night-02.svg, cloudy-night-outline-01.svg, cloudy-outline-01.svg, wifi-01.svg, wifi-02.svg, wifi-outline-01.svg
- OS/Platform Logos
  - Generic patterns: android, apple, windows, xbox, playstation
  - icons/: android.svg, apple.svg
  - icons/ionicons-svg/: android-01.svg, apple-01.svg, playstation-01.svg, windows-01.svg, xbox-01.svg

## 2) Specialized Sets (App-Focused)

### 2.1 Sub-Categories Common in Specialized Sets

#### Social & Community

- Social Brands
  - Generic patterns: facebook, instagram, linkedin, twitter, youtube, reddit, tumblr, wordpress, whatsapp, snapchat, vimeo, pinterest, skype, github
  - icons/: None
  - icons/ionicons-svg/: facebook-01.svg, github-01.svg, instagram-01.svg, linkedin-01.svg, pinterest-01.svg, reddit-01.svg, skype-01.svg, snapchat-01.svg, tumblr-01.svg, twitter-01.svg, vimeo-01.svg, whatsapp-01.svg, wordpress-01.svg, youtube-01.svg
- Reactions
  - Generic patterns: heart, thumbs-up, thumbs-down, star, happy, sad
  - icons/: None
  - icons/ionicons-svg/: happy-01.svg, happy-02.svg, happy-outline-01.svg, heart-01.svg, heart-02.svg, heart-outline-01.svg, heart-outline-02.svg, sad-01.svg, sad-02.svg, sad-outline-01.svg, star-01.svg, star-02.svg, star-half-01.svg, star-half-02.svg, star-outline-01.svg, star-outline-02.svg, thumbs-down-01.svg, thumbs-down-02.svg, thumbs-down-outline-01.svg, thumbs-up-01.svg, thumbs-up-02.svg, thumbs-up-outline-01.svg
- Awards
  - Generic patterns: medal, trophy, ribbon, badge
  - icons/: medal-outline.svg
  - icons/ionicons-svg/: medal-01.svg, medal-02.svg, medal-outline-01.svg, ribbon-01.svg, ribbon-02.svg, ribbon-outline-01.svg, trophy-01.svg, trophy-02.svg, trophy-outline-01.svg

#### Commerce & Finance

- Payments
  - Generic patterns: cash, card, wallet, usd, yen, euro, bitcoin, invoice
  - icons/: invoice.svg
  - icons/ionicons-svg/: bitcoin-01.svg, card-01.svg, card-02.svg, card-outline-01.svg, cash-01.svg, cash-02.svg, cash-outline-01.svg, euro-01.svg, usd-01.svg, yen-01.svg
- Shopping
  - Generic patterns: cart, basket, bag, pricetag, pricetags
  - icons/: None
  - icons/ionicons-svg/: basket-01.svg, basket-02.svg, basket-outline-01.svg, basketball-01.svg, basketball-02.svg, basketball-outline-01.svg, cart-01.svg, cart-02.svg, cart-outline-01.svg, pricetag-01.svg, pricetag-02.svg, pricetag-outline-01.svg, pricetags-01.svg, pricetags-02.svg, pricetags-outline-01.svg
- Business
  - Generic patterns: briefcase, calculator, analytics, stats
  - icons/: analytics-outline.svg, analytics.svg, briefcase-outline.svg, calculator-outline.svg, stats-outline.svg
  - icons/ionicons-svg/: analytics-01.svg, analytics-02.svg, analytics-outline-01.svg, briefcase-01.svg, briefcase-02.svg, briefcase-outline-01.svg, calculator-01.svg, calculator-02.svg, calculator-outline-01.svg, stats-01.svg, stats-02.svg, stats-outline-01.svg

#### Productivity & Workflows

- Tasks/Work
  - Generic patterns: work, schedule, calendar, check, report
  - icons/: box-check-no.svg, box-check-yes.svg, calendar-outline.svg, flag-checkered.svg, report-add.svg, reports-flagged-red.svg, reports-flagged-red2.svg, reports-flagged.svg, reports-misc-large.svg, reports-misc.svg, reports-work.svg, reports.original.svg, reports.svg, schedule.svg, shift-reports.svg, work-shift-light.svg, work-shift.svg
  - icons/ionicons-svg/: calendar-01.svg, calendar-02.svg, calendar-outline-01.svg, checkbox-01.svg, checkbox-02.svg, checkbox-outline-01.svg, checkbox-outline-02.svg, checkmark-01.svg, checkmark-02.svg, checkmark-circle-01.svg, checkmark-circle-02.svg, checkmark-circle-outline-01.svg, checkmark-circle-outline-02.svg, code-working-01.svg, code-working-02.svg, git-network-01.svg, git-network-02.svg
- Forms/Editing
  - Generic patterns: form, edit, create, clipboard, paper
  - icons/: clipboard-outline.svg, copy-form.svg, create-outline.svg, information-circle-outline.svg, message-edit-square.svg, message-edit.svg, paper-outline.svg, refresh-form.svg, reset-form.svg
  - icons/ionicons-svg/: clipboard-01.svg, clipboard-02.svg, clipboard-outline-01.svg, create-01.svg, create-02.svg, create-outline-01.svg, information-01.svg, information-02.svg, information-circle-01.svg, information-circle-02.svg, information-circle-outline-01.svg, paper-01.svg, paper-02.svg, paper-outline-01.svg, paper-plane-01.svg, paper-plane-02.svg, paper-plane-outline-01.svg
- Organization
  - Generic patterns: list, table, folder, archive
  - icons/: archive-outline.svg, copy-list.svg, copy-table.svg, folder-open-outline.svg, folder-outline.svg, folder-verified-outline.svg, list-box-outline.svg, tablet-landscape.svg, tablet-portrait.svg
  - icons/ionicons-svg/: archive-01.svg, archive-02.svg, archive-outline-01.svg, folder-01.svg, folder-02.svg, folder-open-01.svg, folder-open-02.svg, folder-open-outline-01.svg, folder-outline-01.svg, list-01.svg, list-02.svg, list-box-01.svg, list-box-02.svg, list-box-outline-01.svg, tablet-landscape-01.svg, tablet-landscape-02.svg, tablet-portrait-01.svg, tablet-portrait-02.svg

#### Developer & Technical

- Code
  - Generic patterns: code, developer, bug, build, git, terminal
  - icons/: developer-head.svg, developer-machine.svg
  - icons/ionicons-svg/: barcode-01.svg, barcode-02.svg, barcode-outline-01.svg, bug-01.svg, bug-02.svg, bug-outline-01.svg, build-01.svg, build-02.svg, build-outline-01.svg, code-01.svg, code-02.svg, code-download-01.svg, code-download-02.svg, code-working-01.svg, code-working-02.svg, codepen-01.svg, git-branch-01.svg, git-branch-02.svg, git-commit-01.svg, git-commit-02.svg, git-compare-01.svg, git-compare-02.svg, git-merge-01.svg, git-merge-02.svg, git-network-01.svg, git-network-02.svg, git-pull-request-01.svg, git-pull-request-02.svg, github-01.svg
- Infrastructure
  - Generic patterns: database, server, cloud, sync
  - icons/: database-refresh.svg, sync.svg
  - icons/ionicons-svg/: cloud-01.svg, cloud-02.svg, cloud-circle-01.svg, cloud-circle-02.svg, cloud-circle-outline-01.svg, cloud-done-01.svg, cloud-done-02.svg, cloud-done-outline-01.svg, cloud-download-01.svg, cloud-download-02.svg, cloud-download-outline-01.svg, cloud-outline-01.svg, cloud-outline-02.svg, cloud-upload-01.svg, cloud-upload-02.svg, cloud-upload-outline-01.svg, cloudy-01.svg, cloudy-02.svg, cloudy-night-01.svg, cloudy-night-02.svg, cloudy-night-outline-01.svg, cloudy-outline-01.svg, sync-01.svg, sync-02.svg
- Security
  - Generic patterns: lock, unlock, key, shield
  - icons/: keypad-outline.svg
  - icons/ionicons-svg/: clock-01.svg, clock-02.svg, clock-outline-01.svg, key-01.svg, key-02.svg, key-outline-01.svg, keypad-01.svg, keypad-02.svg, keypad-outline-01.svg, lock-01.svg, lock-02.svg, lock-outline-01.svg, unlock-01.svg, unlock-02.svg, unlock-outline-01.svg

#### Media & Creative

- Image/Photo
  - Generic patterns: image, images, photo, camera
  - icons/: image-outline.svg, images-outline.svg, photos-outline.svg
  - icons/ionicons-svg/: camera-01.svg, camera-02.svg, camera-outline-01.svg, image-01.svg, image-02.svg, image-outline-01.svg, images-01.svg, images-02.svg, images-outline-01.svg, photos-01.svg, photos-02.svg, photos-outline-01.svg, reverse-camera-01.svg, reverse-camera-02.svg, reverse-camera-outline-01.svg
- Audio/Video
  - Generic patterns: mic, microphone, volume, videocam, play, pause, recording, rewind, fastforward
  - icons/: None
  - icons/ionicons-svg/: fastforward-01.svg, fastforward-02.svg, fastforward-outline-01.svg, mic-01.svg, mic-02.svg, mic-off-01.svg, mic-off-02.svg, mic-off-outline-01.svg, mic-outline-01.svg, microphone-01.svg, microphone-02.svg, microphone-outline-01.svg, pause-01.svg, pause-02.svg, pause-outline-01.svg, play-01.svg, play-02.svg, play-outline-01.svg, playstation-01.svg, recording-01.svg, recording-02.svg, recording-outline-01.svg, rewind-01.svg, rewind-02.svg, rewind-outline-01.svg, videocam-01.svg, videocam-02.svg, videocam-outline-01.svg, volume-down-01.svg, volume-down-02.svg, volume-mute-01.svg, volume-mute-02.svg, volume-off-01.svg, volume-off-02.svg, volume-up-01.svg, volume-up-02.svg
- Design Tools
  - Generic patterns: brush, color, crop, resize, contrast, flask
  - icons/: resize.svg
  - icons/ionicons-svg/: brush-01.svg, brush-02.svg, brush-outline-01.svg, color-fill-01.svg, color-fill-02.svg, color-fill-outline-01.svg, color-filter-01.svg, color-filter-02.svg, color-filter-outline-01.svg, color-palette-01.svg, color-palette-02.svg, color-palette-outline-01.svg, color-wand-01.svg, color-wand-02.svg, color-wand-outline-01.svg, contrast-01.svg, contrast-02.svg, crop-01.svg, crop-02.svg, crop-outline-01.svg, flask-01.svg, flask-02.svg, flask-outline-01.svg, microphone-01.svg, microphone-02.svg, microphone-outline-01.svg, resize-01.svg, resize-02.svg

#### Industry & Domain-Specific

- Energy/Oilfield
  - Generic patterns: oil, frack, derrick, truck-diesel
  - icons/: frack-truck.svg, fracking-detail.svg, fracking-well.svg, oil-derrick-problem.svg, oil-derrick-warning.svg, oil-derrick.svg, oil-location.svg, truck-diesel.svg
  - icons/ionicons-svg/: None
- Transport/Logistics
  - Generic patterns: car, bus, subway, train, boat, plane, truck
  - icons/: frack-truck.svg, truck-diesel.svg
  - icons/ionicons-svg/: boat-01.svg, boat-02.svg, boat-outline-01.svg, bus-01.svg, bus-02.svg, bus-outline-01.svg, car-01.svg, car-02.svg, car-outline-01.svg, card-01.svg, card-02.svg, card-outline-01.svg, cart-01.svg, cart-02.svg, cart-outline-01.svg, paper-plane-01.svg, paper-plane-02.svg, paper-plane-outline-01.svg, plane-01.svg, plane-02.svg, plane-outline-01.svg, planet-01.svg, planet-02.svg, planet-outline-01.svg, subway-01.svg, subway-02.svg, subway-outline-01.svg, train-01.svg, train-02.svg, train-outline-01.svg
- Health & Medical
  - Generic patterns: medical, medkit, pulse, thermometer
  - icons/: pulse-outline.svg, pulse.svg
  - icons/ionicons-svg/: medical-01.svg, medical-02.svg, medical-outline-01.svg, medkit-01.svg, medkit-02.svg, medkit-outline-01.svg, pulse-01.svg, pulse-02.svg, pulse-outline-01.svg, thermometer-01.svg, thermometer-02.svg, thermometer-outline-01.svg

## 3) Notes on Matching Logic

- Matching is substring-based, case-insensitive.
- A file can appear in multiple groups when names overlap (expected).
- This is intended as a practical naming index, not a strict ontology.
