# TODOS: Fix Entity Creation Scripts

## Issues Identified
- Scripts create entities with many missing required values
- Status updates don't match expected dropdown values
- Status values are outside the desired range/enum values
- Design script works correctly (use as reference)

## Action Items

### 1. Review Design Script Pattern
- [ ] Examine design script to understand correct entity creation pattern
- [ ] Document required fields and their expected format
- [ ] Note how design script handles status dropdown values

### 2. Fix Status Field Issues
- [ ] Identify the correct status enum/dropdown values
- [ ] Update scripts to use only valid status values from the dropdown
- [ ] Ensure status field uses the correct data type (enum vs string)
- [ ] Add validation to reject invalid status values

### 3. Fix Missing Values
- [ ] Create a checklist of all required fields per entity type
- [ ] Add default values for optional fields where appropriate
- [ ] Implement validation to ensure required fields are populated
- [ ] Add error handling for missing critical data

### 4. Standardize Scripts
- [ ] Apply design script patterns to other entity creation scripts
- [ ] Create reusable functions for common field mappings
- [ ] Add comprehensive validation before entity creation
- [ ] Test each script with edge cases

### 5. Testing
- [ ] Verify all status values are within valid dropdown range
- [ ] Confirm no required fields are missing
- [ ] Compare output entities with design script results
- [ ] Document expected vs actual field values for debugging
