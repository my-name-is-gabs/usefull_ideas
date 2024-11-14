# Get some help

### Testing with localStorage in vue
```javascript
import { shallowMount } from '@vue/test-utils';
import SampleComponent from '@/components/SampleComponent.vue';

describe('SampleComponent', () => {
  beforeEach(() => {
    // Reset the mock before each test
    jest.clearAllMocks();
  });

  it('should set registeredUser to staticData when localStorage is empty', () => {
    // Mock localStorage to return null
    jest.spyOn(Storage.prototype, 'getItem').mockReturnValue(null);

    const wrapper = shallowMount(SampleComponent);
    expect(wrapper.vm.registeredUser).toEqual([{ ...staticData }]);
  });

  it('should parse users from localStorage if available', () => {
    // Mock localStorage with JSON data
    const mockUsers = [{ id: 1, name: 'John Doe' }];
    jest.spyOn(Storage.prototype, 'getItem').mockReturnValue(JSON.stringify(mockUsers));

    const wrapper = shallowMount(SampleComponent);
    expect(wrapper.vm.registeredUser).toEqual(mockUsers);
  });

  it('should handle invalid JSON gracefully', () => {
    // Mock localStorage to return invalid JSON
    jest.spyOn(Storage.prototype, 'getItem').mockReturnValue("invalid-json");

    expect(() => shallowMount(SampleComponent)).toThrow();
  });
});

```
