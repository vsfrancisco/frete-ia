document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-simulacao');
    const resultado = document.getElementById('resultado');
    const listarBtn = document.getElementById('listar-btn');
    const modal = document.getElementById('modal-transp');
    const btnNovaTransp = document.getElementById('btn-nova-transp');
    const formTransp = document.getElementById('form-transp');
    
    // Carregar transportadoras (com tratamento de erro)
    async function carregarTransportadoras() {
        const select = document.getElementById('transportadora_id');
        try {
            const response = await fetch('/transportadoras');
            if (!response.ok) throw new Error('Erro na API');
            const transportadoras = await response.json();
            
            select.innerHTML = '<option value="">Selecione uma transportadora</option>';
            if (transportadoras.length === 0) {
                select.innerHTML += '<option disabled>Nenhuma transportadora cadastrada</option>';
            } else {
                transportadoras.forEach(t => {
                    select.innerHTML += `<option value="${t.id}">${t.nome} (${t.consumo_km_l}km/L, ${t.margem_percentual}%)</option>`;
                });
            }
        } catch (error) {
            console.error('Erro ao carregar transportadoras:', error);
            select.innerHTML = '<option value="">Erro ao carregar</option>';
        }
    }
    
    // Calcular frete
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const dados = {
            transportadora_id: parseInt(document.getElementById('transportadora_id').value),
            origem: document.getElementById('origem').value,
            destino: document.getElementById('destino').value,
            distancia_km: parseFloat(document.getElementById('distancia_km').value),
            peso_kg: parseFloat(document.getElementById('peso_kg').value)
        };
        
        if (!dados.transportadora_id || dados.transportadora_id === 0) {
            alert('⚠️ Selecione uma transportadora primeiro!');
            return;
        }
        
        try {
            const response = await fetch('/simulacoes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados)
            });
            
            if (!response.ok) throw new Error(await response.text());
            
            const simulacao = await response.json();
            
            // Mostra resultado
            document.getElementById('custo_diesel').textContent = `R$ ${simulacao.custo_diesel.toFixed(2)}`;
            document.getElementById('custo_manutencao').textContent = `R$ ${simulacao.custo_manutencao.toFixed(2)}`;
            document.getElementById('custo_total').textContent = `R$ ${simulacao.custo_total.toFixed(2)}`;
            document.getElementById('preco_sugerido').textContent = `R$ ${simulacao.preco_sugerido.toFixed(2)}`;
            document.getElementById('simulacao_id').textContent = simulacao.id;

            // ADICIONE ESTA LINHA PARA O PISO ANTT:
const pisoElement = document.getElementById('piso_anttt');
if (pisoElement) {
    pisoElement.textContent = sim.piso_anttt && sim.piso_anttt > 0 
        ? `R$ ${sim.piso_anttt.toFixed(2)}` 
        : 'Sem Piso (0)';
}
            
            resultado.classList.remove('hidden');
            resultado.scrollIntoView({ behavior: 'smooth' });
            listarSimulacoes();
            
        } catch (error) {
            alert('Erro ao calcular: ' + error.message);
        }
    });
    
    // Listar simulações
    listarBtn.addEventListener('click', listarSimulacoes);
    
    async function listarSimulacoes() {
        try {
            const response = await fetch('/simulacoes');
            const simulacoes = await response.json();
            
            const historico = document.getElementById('historico');
            historico.innerHTML = simulacoes.length === 0 
                ? '<p style="color: #7f8c8d;">Nenhuma simulação ainda</p>'
                : '';
            
            simulacoes.slice(0, 10).forEach(sim => {
                const div = document.createElement('div');
                div.className = 'historico-item';
                div.innerHTML = `
                    <strong>${sim.origem} → ${sim.destino}</strong><br>
                    <small>${sim.distancia_km.toFixed(0)}km | ${sim.peso_kg.toFixed(0)}kg | 
                    <strong>R$ ${sim.preco_sugerido.toFixed(2)}</strong></small><br>
                    <span style="font-size: 12px; color: #7f8c8d;">ID: ${sim.id}</span>
                `;
                historico.appendChild(div);
            });
        } catch (error) {
            console.error('Erro ao listar:', error);
        }
    }
    
    // Modal nova transportadora
    btnNovaTransp.addEventListener('click', () => {
        modal.classList.remove('hidden');
        document.getElementById('transp-nome').focus();
    });
    
    document.getElementById('fechar-modal').addEventListener('click', () => {
        modal.classList.add('hidden');
        formTransp.reset();
    });

    document.getElementById('piso_anttt').textContent = `R$ ${sim.piso_anttt?.toFixed(2) || 'N/A'}`;

    
    // Fechar modal clicando fora
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
            formTransp.reset();
        }
    });
    
    formTransp.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const dados = {
            nome: document.getElementById('transp-nome').value,
            consumo_km_l: parseFloat(document.getElementById('transp-consumo').value),
            margem_percentual: parseFloat(document.getElementById('transp-margem').value),
            custo_manutencao_por_km: parseFloat(document.getElementById('transp-manutencao').value)
        };
        
        try {
            const response = await fetch('/transportadoras', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados)
            });
            
            if (!response.ok) throw new Error(await response.text());
            
            modal.classList.add('hidden');
            formTransp.reset();
            carregarTransportadoras();
            alert('✅ Transportadora criada!');
            
        } catch (error) {
            alert('Erro ao salvar: ' + error.message);
        }
    });
    
    // Inicialização
    carregarTransportadoras();
    listarSimulacoes();
});
