# Querys SQL

# Conta corrente dos sócios (não usado)
sql_accounts = "select gs.socio_id, gs.nsocio, gs.nome, sum(gc.valor_em_divida) divida, sum(gc.valor_regularizado) regularizado, \
                'Comparticipação' descricao from gestaugi_socios gs \
				inner join gestaugi_comparticipacoes gc on (gs.socio_id = gc.socio_id) \
				where gc.valor_em_divida > 0 GROUP by gs.nome \
				union ALL \
				select gs.socio_id, gs.nsocio, gs.nome, sum(ga.anuidade) divida , 0 as regularizado,  'Anuidade'  as descricao \
				from gestaugi_socios gs inner join gestaugi_anuidades ga on (gs.socio_id = ga.socio_id) \
				where ga.dt_pagamento ISNULL GROUP by gs.nome \
				order by gs.nome "

# Dividas dos sócios
sql_debts = "select gs.socio_id, gs.nsocio ,gs.nome, gs.lotes , gs.anuidivida ,gs.compdivida, \
             (select COALESCE(sum(gp.pagamento),0) from gestaugi_pagamentos gp where gp.socio_id = gs.socio_id \
              and gp.tipo='Comparticipação') as compartpag, gs.estado \
              from gestaugi_socios gs"

# Dividas dos sócios (não apanha todos os registo)
sql_debts2 = "select gs.socio_id, gs.nsocio ,gs.nome, gs.lotes , gs.anuidivida ,gs.compdivida, 0 as compartpag, gs.estado \
            from gestaugi_socios gs \
            left outer join gestaugi_pagamentos gp on (gs.socio_id = gp.socio_id) \
            where gp.tipo is NULL \
            union all \
            select gs.socio_id, gs.nsocio ,gs.nome, gs.lotes , gs.anuidivida ,gs.compdivida, sum(gp.pagamento) as compartpag, gs.estado \
            from gestaugi_socios gs \
            left outer join gestaugi_pagamentos gp on (gs.socio_id = gp.socio_id) \
            where gp.tipo = 'Comparticipação' \
            order by gs.nsocio"

# Despesas por tipo de despesa, por ano
sql_expenses = "select ano, despesa, dt_registo,descricao, despesa_id from ( \
                select '1' coluna, despesa_id, ano sep,'' || ano as ano, despesa, dt_registo, gt.descricao \
                from gestaugi_despesas gd \
                inner join gestaugi_tiposdespesas gt on (gt.tipo_id = gd.tipo_id) \
                union \
                select '2' coluna,sum(despesa_id), ano sep, 'Subtotal ' || ano as ano, sum(despesa) as despesa, NULL as dt_registo, '' as descricao \
                from gestaugi_despesas gd \
                group by ano \
                union \
                select '99' coluna, sum(despesa_id), 9999 sep, 'Total' as ano, sum(despesa) as despesa, NULL as dt_registo, '' as descricao \
                from gestaugi_despesas gd) \
                as res order by case when coluna ='99' then 1 else 0 end, sep, coluna"

# Despesas por tipo de despesa, por ano
sql_totexpenses = "select despesa_id, descricao, despesa from ( \
                   select '1' coluna, gd.despesa_id,gt.descricao, sum(gd.despesa) as despesa \
                   from gestaugi_despesas gd \
                   inner join gestaugi_tiposdespesas gt on (gt.tipo_id = gd.tipo_id) \
                   GROUP by gd.despesa_id, gt.descricao \
                   union ALL \
                   select '99' coluna, sum(gd.despesa_id), 'Total' as descricao, sum(gd.despesa) \
                   from gestaugi_despesas gd) as despesas \
                   ORDER by coluna"

# Áreas dos lotes dos sócios
sql_areas = "select gs.socio_id, gs.nsocio, gs.nome, sum(area) as area \
             from gestaugi_socios gs \
             left outer join gestaugi_lotes gl on (gl.socio_id=gs.socio_id) \
             group by gs.socio_id,gs.nsocio \
             order by gs.nome"

# Pagamentos totais dos sócios
sql_payments = "select gs.socio_id, gs.nome, gp.pagamento_id, \
               case when tipo = 'Anuidade' \
                  then sum(pagamento) \
                  else 0 \
               end as anuidades, \
               case when tipo = 'Comparticipação' \
                  then sum(pagamento) \
                  else 0 \
               end as comparticipacoes \
               from gestaugi_socios gs \
               inner join gestaugi_pagamentos gp on (gp.socio_id = gs.socio_id) \
               group by gs.socio_id \
               order by gs.nome"