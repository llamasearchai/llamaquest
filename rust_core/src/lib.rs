use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

/// A Rust module providing performance-critical functionality for LlamaQuest
#[pymodule]
fn llamaquest_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_pathfinding, m)?)?;
    m.add_function(wrap_pyfunction!(collision_detection, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_field_of_view, m)?)?;
    m.add_class::<PhysicsEngine>()?;
    Ok(())
}

/// Calculate optimal path between two points using A* algorithm
#[pyfunction]
fn calculate_pathfinding(
    start_x: usize, start_y: usize,
    end_x: usize, end_y: usize,
    walkable_map: Vec<Vec<bool>>,
    max_steps: Option<usize>
) -> PyResult<Vec<(usize, usize)>> {
    // Simple implementation - to be expanded with proper A* algorithm
    
    // For now, just return a direct path ignoring obstacles
    let mut path = Vec::new();
    let steps = max_steps.unwrap_or(1000);
    
    let dx = if start_x < end_x { 1 } else if start_x > end_x { -1 } else { 0 };
    let dy = if start_y < end_y { 1 } else if start_y > end_y { -1 } else { 0 };
    
    let mut current_x = start_x as isize;
    let mut current_y = start_y as isize;
    
    path.push((start_x, start_y));
    
    for _ in 0..steps {
        if current_x == end_x as isize && current_y == end_y as isize {
            break;
        }
        
        if current_x != end_x as isize {
            current_x += dx;
        }
        
        if current_y != end_y as isize {
            current_y += dy;
        }
        
        // Safety check for boundaries
        if current_x < 0 || current_y < 0 || 
           current_x >= walkable_map[0].len() as isize || 
           current_y >= walkable_map.len() as isize {
            break;
        }
        
        // Check if position is walkable
        if !walkable_map[current_y as usize][current_x as usize] {
            // In a real implementation, we would find a way around
            break;
        }
        
        path.push((current_x as usize, current_y as usize));
    }
    
    Ok(path)
}

/// Fast collision detection between entities
#[pyfunction]
fn collision_detection(
    entity1_x: f32, entity1_y: f32, entity1_width: f32, entity1_height: f32,
    entity2_x: f32, entity2_y: f32, entity2_width: f32, entity2_height: f32
) -> PyResult<bool> {
    // Axis-Aligned Bounding Box collision detection
    let collision = 
        entity1_x < entity2_x + entity2_width &&
        entity1_x + entity1_width > entity2_x &&
        entity1_y < entity2_y + entity2_height &&
        entity1_y + entity1_height > entity2_y;
    
    Ok(collision)
}

/// Calculate field of view for the player
#[pyfunction]
fn calculate_field_of_view(
    origin_x: usize, origin_y: usize,
    radius: usize,
    obstacle_map: Vec<Vec<bool>>
) -> PyResult<Vec<Vec<bool>>> {
    // Create a visibility map initialized to false
    let height = obstacle_map.len();
    let width = if height > 0 { obstacle_map[0].len() } else { 0 };
    
    let mut visibility_map = vec![vec![false; width]; height];
    
    // Mark the origin as visible
    if origin_y < height && origin_x < width {
        visibility_map[origin_y][origin_x] = true;
    }
    
    // Basic raycasting algorithm
    // In a real implementation, this would use a more sophisticated algorithm
    // such as recursive shadowcasting for better performance
    
    // Cast rays in a circle
    for angle in 0..360 {
        let angle_rad = angle as f32 * std::f32::consts::PI / 180.0;
        let mut ray_x = origin_x as f32;
        let mut ray_y = origin_y as f32;
        
        for step in 1..=radius {
            ray_x += angle_rad.cos();
            ray_y += angle_rad.sin();
            
            let tile_x = ray_x.round() as usize;
            let tile_y = ray_y.round() as usize;
            
            // Check boundaries
            if tile_y >= height || tile_x >= width {
                break;
            }
            
            // Mark as visible
            visibility_map[tile_y][tile_x] = true;
            
            // Stop if hit obstacle
            if obstacle_map[tile_y][tile_x] {
                break;
            }
        }
    }
    
    Ok(visibility_map)
}

/// Physics engine for game entities
#[pyclass]
struct PhysicsEngine {
    gravity: f32,
    friction: f32,
}

#[pymethods]
impl PhysicsEngine {
    #[new]
    fn new(gravity: Option<f32>, friction: Option<f32>) -> Self {
        PhysicsEngine {
            gravity: gravity.unwrap_or(9.8),
            friction: friction.unwrap_or(0.1),
        }
    }
    
    /// Apply physics to an entity's velocity and position
    fn update_entity(&self, 
        position_x: f32, position_y: f32,
        velocity_x: f32, velocity_y: f32,
        is_on_ground: bool,
        delta_time: f32
    ) -> PyResult<((f32, f32), (f32, f32))> {
        // Apply gravity if not on ground
        let mut new_velocity_y = velocity_y;
        if !is_on_ground {
            new_velocity_y += self.gravity * delta_time;
        }
        
        // Apply friction
        let mut new_velocity_x = velocity_x;
        if is_on_ground {
            // Apply friction only when on ground
            if velocity_x > 0.0 {
                new_velocity_x = (velocity_x - self.friction * delta_time).max(0.0);
            } else if velocity_x < 0.0 {
                new_velocity_x = (velocity_x + self.friction * delta_time).min(0.0);
            }
        }
        
        // Update position
        let new_position_x = position_x + new_velocity_x * delta_time;
        let new_position_y = position_y + new_velocity_y * delta_time;
        
        Ok(((new_position_x, new_position_y), (new_velocity_x, new_velocity_y)))
    }
    
    /// Calculate projectile trajectory
    fn calculate_projectile_path(
        &self,
        start_x: f32, start_y: f32,
        velocity_x: f32, velocity_y: f32,
        time_steps: usize,
        delta_time: f32
    ) -> PyResult<Vec<(f32, f32)>> {
        let mut path = Vec::with_capacity(time_steps);
        let mut pos_x = start_x;
        let mut pos_y = start_y;
        let mut vel_x = velocity_x;
        let mut vel_y = velocity_y;
        
        path.push((pos_x, pos_y));
        
        for _ in 0..time_steps {
            // Apply air resistance (simplified)
            vel_x *= (1.0 - 0.01 * delta_time);
            
            // Apply gravity
            vel_y += self.gravity * delta_time;
            
            // Update position
            pos_x += vel_x * delta_time;
            pos_y += vel_y * delta_time;
            
            path.push((pos_x, pos_y));
        }
        
        Ok(path)
    }
    
    /// Check if an entity can move to a new position
    fn can_move_to(
        &self,
        entity_x: f32, entity_y: f32,
        entity_width: f32, entity_height: f32,
        new_x: f32, new_y: f32,
        obstacles: Vec<(f32, f32, f32, f32)>
    ) -> PyResult<bool> {
        // Check for collisions with obstacles
        for (obs_x, obs_y, obs_width, obs_height) in obstacles {
            let collision = 
                new_x < obs_x + obs_width &&
                new_x + entity_width > obs_x &&
                new_y < obs_y + obs_height &&
                new_y + entity_height > obs_y;
                
            if collision {
                return Ok(false);
            }
        }
        
        Ok(true)
    }
} 