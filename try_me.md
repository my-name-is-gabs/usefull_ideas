# Get some help

### Some idea in mocking localStorage
```
// tests/SampleComponent.test.js
import { shallowMount } from '@vue/test-utils';
import SampleComponent from '@/components/SampleComponent.vue';

describe('SampleComponent.vue', () => {
  const staticData = { key: 'defaultData' };

  beforeEach(() => {
    jest.clearAllMocks(); // Clear mocks before each test to avoid interference
  });

  it('should initialize myarray with data from localStorage if valid JSON exists', () => {
    // Mock localStorage to return a valid JSON string
    const localStorageData = JSON.stringify([{ key: 'value' }]);
    jest.spyOn(global.localStorage, 'getItem').mockReturnValue(localStorageData);

    const wrapper = shallowMount(SampleComponent);
    expect(wrapper.vm.myarray).toEqual([{ key: 'value' }]);
  });

  it('should initialize myarray with static data if localStorage data is null', () => {
    // Mock localStorage to return null
    jest.spyOn(global.localStorage, 'getItem').mockReturnValue(null);

    const wrapper = shallowMount(SampleComponent);
    expect(wrapper.vm.myarray).toEqual([{ ...staticData }]);
  });

  it('should initialize myarray as an empty array if JSON parsing fails', () => {
    // Mock localStorage to return an invalid JSON string
    jest.spyOn(global.localStorage, 'getItem').mockReturnValue('invalid JSON');

    const wrapper = shallowMount(SampleComponent);
    expect(wrapper.vm.myarray).toEqual([]);
  });
});
```

### Testing with localStorage
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
