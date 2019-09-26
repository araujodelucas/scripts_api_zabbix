select 
data,
eventid,
hostid,
host,
group_name,
case
when severity like '0' then 'Not classified'
when severity like '1' then 'Information'
when severity like '2' then 'Warning'
when severity like '3' then 'Average'
when severity like '4' then 'High'
when severity like '5' then 'Disaster'
else severity
end as severity,
Error as triggers,
case
when ack like '0' then 'No'
when ack like '1' then 'Yes'
else ack
end as ack,
data_ack,
ack_message,
user_ack,
action_name,
sum(Incidents) as number_changes 
from (
 Select 
   to_char(to_timestamp(events.clock)::TIMESTAMP without TIME zone, 'DD-MM-YYYY hh24:mi:ss') AS data,
   events.eventid as eventid,
   hosts.hostid as hostid,
   hosts.name as host,
   --groups.name as group_name,
   string_agg(Distinct groups.name, ';') as group_name,
   trim(to_char(triggers.priority,'9')) as severity,
   triggers.description as Error,
   trim(to_char(events.acknowledged,'9')) as ack,
   string_agg(to_char(to_timestamp(acknowledges.clock)::TIMESTAMP without TIME zone, 'DD-MM-YYYY hh24:mi:ss'),';') AS data_ack,
   string_agg(acknowledges.message,';') as ack_message,
   string_agg(users.alias,';') as user_ack,
   --acknowledges.message as ack_message,
   string_agg(distinct actions.name, ';') as action_name,
   Count(Distinct events.eventid) As Incidents
 From
   triggers Inner Join
   events On events.objectid = triggers.triggerid Inner Join
   functions On functions.triggerid = triggers.triggerid Inner Join
   items On items.itemid = functions.itemid Inner Join
   hosts On items.hostid = hosts.hostid Inner Join
   hosts_groups On hosts.hostid = hosts_groups.hostid inner join 
   groups on hosts_groups.groupid = groups.groupid left join
   acknowledges on acknowledges.eventid = events.eventid left join
   alerts on alerts.eventid = events.eventid  left join
   actions on actions.actionid = alerts.actionid left join
   users on users.userid=acknowledges.userid
 Where
  --events.objectid not in (select triggerid from triggers) and
   triggers.flags In ('0', '4') and
   events.source = 0 and
   events.object = 0  and
   --groups.name in('DB Servers Oracle','DB Servers SQL Server','Instances Oracle','Instances SQL Server','Middleware/DB Servers','Middleware Servers') and
   to_date(to_char(date_trunc('day', to_timestamp(events.clock))::TIMESTAMP without TIME zone, 'YYYY-MM-DD'), 'YYYY-MM-DD') between to_date('2019-08-10','YYYY-MM-DD') and to_date('2019-08-15','YYYY-MM-DD')
 Group By
   events.eventid,
    hosts.hostid,
    hosts.name,
   -- groups.name,
    triggers.priority,
    triggers.description,
    events.acknowledged,
    --acknowledges.clock,
    --acknowledges.message,
    events.clock
 Order By
 1 Desc) tab
group by eventid,
hostid,
host,
group_name,
severity,
triggers,
ack,
data_ack,
ack_message,
user_ack,
action_name,
data 
Order by to_date(data,'DD-MM-YYYY HH24');