// Carrito de compras
class Cart {
    constructor() {
        this.items = [];
        this.total = 0;
    }

    addItem(product) {
        const existingItem = this.items.find(item => item.id === product.id);
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            this.items.push({ ...product, quantity: 1 });
        }
        this.calculateTotal();
        this.updateCartUI();
    }

    removeItem(productId) {
        this.items = this.items.filter(item => item.id !== productId);
        this.calculateTotal();
        this.updateCartUI();
    }

    updateQuantity(productId, quantity) {
        const item = this.items.find(item => item.id === productId);
        if (item) {
            item.quantity = parseInt(quantity);
            if (item.quantity <= 0) {
                this.removeItem(productId);
            }
        }
        this.calculateTotal();
        this.updateCartUI();
    }

    calculateTotal() {
        this.total = this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    }

    updateCartUI() {
        const cartContainer = document.getElementById('cart-items');
        const totalElement = document.getElementById('cart-total');
        
        if (cartContainer) {
            cartContainer.innerHTML = this.items.map(item => `
                <div class="cart-item" data-id="${item.id}">
                    <span>${item.name}</span>
                    <input type="number" value="${item.quantity}" min="0" 
                           onchange="cart.updateQuantity(${item.id}, this.value)">
                    <span>$${(item.price * item.quantity).toFixed(2)}</span>
                    <button onclick="cart.removeItem(${item.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `).join('');
        }
        
        if (totalElement) {
            totalElement.textContent = `Total: $${this.total.toFixed(2)}`;
        }
    }

    clear() {
        this.items = [];
        this.total = 0;
        this.updateCartUI();
    }
}

// Inicializar carrito
const cart = new Cart();

// Funciones para la interfaz de usuario
document.addEventListener('DOMContentLoaded', () => {
    // Manejar clicks en botones de agregar al carrito
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', (e) => {
            const productCard = e.target.closest('.menu-item');
            const product = {
                id: parseInt(productCard.dataset.id),
                name: productCard.querySelector('.menu-item-name').textContent,
                price: parseFloat(productCard.querySelector('.menu-item-price').dataset.price)
            };
            cart.addItem(product);
            showNotification('Producto agregado al carrito');
        });
    });

    // Manejar envío de pedidos
    const orderForm = document.getElementById('order-form');
    if (orderForm) {
        orderForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (cart.items.length === 0) {
                showNotification('El carrito está vacío', 'error');
                return;
            }

            try {
                const response = await fetch('/api/pedido', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        items: cart.items,
                        total: cart.total,
                        mesa_id: orderForm.dataset.mesaId
                    })
                });

                const data = await response.json();
                if (response.ok) {
                    showNotification('Pedido enviado exitosamente', 'success');
                    cart.clear();
                } else {
                    throw new Error(data.message);
                }
            } catch (error) {
                showNotification(error.message, 'error');
            }
        });
    }
});

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    
    const container = document.querySelector('.container');
    container.insertBefore(notification, container.firstChild);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Función para actualizar estado de mesas
async function updateMesaStatus(mesaId, nuevoEstado) {
    try {
        const response = await fetch(`/api/mesa/${mesaId}/estado`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ estado: nuevoEstado })
        });

        const data = await response.json();
        if (response.ok) {
            showNotification('Estado actualizado exitosamente', 'success');
            // Actualizar UI si es necesario
            const mesaElement = document.querySelector(`[data-mesa-id="${mesaId}"]`);
            if (mesaElement) {
                mesaElement.dataset.estado = nuevoEstado;
                mesaElement.querySelector('.mesa-estado').textContent = nuevoEstado;
            }
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

// Función para actualizar en tiempo real (se puede integrar con WebSocket más adelante)
function initializeRealTimeUpdates() {
    // Aquí se implementará la lógica de WebSocket para actualizaciones en tiempo real
    console.log('Inicializando actualizaciones en tiempo real...');
} 